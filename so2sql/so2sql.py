import math

from time import sleep

from stackapi import StackAPI

from .models import Base, Question, Comment, Answer
from .utils import Utils


class So2Sql:
    def __init__(self,
                 db_session,
                 stack_api_key=None,
                 target_questions=1000,
                 target_questions_per_page=100,
                 default_page_size=100,
                 from_date_string='01-01-2023',
                 to_date_string='31-12-2023',
                 cool_down_time=20,
                 maximum_question_retries=3,
                 questions_filter='!G(XS1)PpTDrxEP7Qbnkh7YPYaI',
                 questions_count_filter_1=[],
                 questions_count_filter_2=[]
                 ):
        self.db_session = db_session
        self.stack_api_key = stack_api_key

        self.TARGET_QUESTIONS = target_questions
        self.TARGET_QUESTIONS_PER_PAGE = target_questions_per_page
        self.DEFAULT_PAGE_SIZE = default_page_size
        self.FROM_DATE_STRING = from_date_string
        self.TO_DATE_STRING = to_date_string
        self.COOL_DOWN_TIME = cool_down_time

        self.maximum_question_retries = maximum_question_retries
        self.questions_filter = questions_filter
        self.questions_count_filter_1 = questions_count_filter_1
        self.questions_count_filter_2 = questions_count_filter_2

        self.question_ids_for_answers = []
        self.cumulative_total_answers_for_questions = []

        self.question_ids_for_comments = []
        self.cumulative_total_comments_for_questions = []

        self.SITE = self.create_stack_api()

    def create_stack_api(self):
        return StackAPI('stackoverflow', key=self.stack_api_key)

    # Function to drop all tables in the database
    def drop_tables(self):
        Base.metadata.drop_all(self.db_session.bind)

    # Function to create all tables in the database
    def create_tables(self):
        Base.metadata.create_all(self.db_session.bind)

    # Function to drop and create all tables in the database
    def drop_and_create_tables(self):
        self.drop_tables()
        self.create_tables()

    # Function to fetch questions from StackOverflow API
    # Endpoint URL: https://api.stackexchange.com/2.3/questions
    # Docs URL: https://api.stackexchange.com/docs/questions
    def fetch_questions_data(self):
        # Defines the maximum number of pages to fetch.
        self.SITE.max_pages = self.TARGET_QUESTIONS / self.TARGET_QUESTIONS_PER_PAGE
        self.SITE.page_size = self.TARGET_QUESTIONS_PER_PAGE

        questions_retries_counter = 0
        questions_counter = 0
    
        # To track the cumulative total of answers & comments for each question. Of course we start from 0
        prev_answers_count = 0
        prev_comments_count = 0
        
        while questions_retries_counter < self.maximum_question_retries and questions_counter < self.TARGET_QUESTIONS:
            # Use stack api to fetch the questions. The library handles pagination for us and returns when all pages are fetched
            questions = self.SITE.fetch(
                'questions',
                sort='votes',
                order='desc',
                filter=self.questions_filter,
                fromdate=Utils.convert_date_time_to_unix_timestamp(
                    self.FROM_DATE_STRING),
                todate=Utils.convert_date_time_to_unix_timestamp(
                    self.TO_DATE_STRING)
            )


            for question in questions['items']:
                if questions_counter >= self.TARGET_QUESTIONS:
                    break
                
                question_title = question.get('title').lower()
                question_body = Utils.remove_html_tags(question.get('body')).lower()

                # Only insert questions that contain the filter words in the title or body
                if len(self.questions_count_filter_1) > 0 and len(self.questions_count_filter_2) > 0:
                    title_matches = any(word in question_title for word in self.questions_count_filter_1) or any(word in question_title for word in self.questions_count_filter_1)
                    body_matches = any(word in question_body for word in self.questions_count_filter_1) or any(word in question_body for word in self.questions_count_filter_2)

                    if not (title_matches or body_matches):
                        continue

                questions_counter += 1

                # Add question ids to the lists if they have answers
                answer_count = int(question.get('answer_count', 0))
                comment_count = int(question.get('comment_count', 0))
                view_count = int(question.get('view_count', 0))

                if answer_count > 0:
                    self.question_ids_for_answers.append(
                        question['question_id'])

                    curr_answers_count = answer_count + prev_answers_count
                    self.cumulative_total_answers_for_questions.append(
                        curr_answers_count)
                    prev_answers_count = curr_answers_count

                # Add question ids to the lists if they have comments
                if comment_count > 0:
                    self.question_ids_for_comments.append(
                        question['question_id'])

                    curr_comments_count = comment_count + prev_comments_count
                    self.cumulative_total_comments_for_questions.append(
                        curr_comments_count)
                    prev_comments_count = curr_comments_count

                tags = question.get('tags')
                tags_str = ""

                if isinstance(tags, tuple):
                    tags_str = ",".join(tags)
                elif isinstance(tags, list):
                    tags_str = ",".join(tags)
                else:
                    tags_str = str(tags).strip("[]")

                # Insert questions data
                self.db_session.add(Question(
                    question_id=question.get('question_id'),
                    title=question_title,
                    body=question_body,
                    creation_date=question.get('creation_date'),
                    last_edit_date=question.get('last_edit_date'),
                    last_activity_date=question.get('last_activity_date'),
                    score=question.get('score'),
                    answer_count=answer_count,
                    view_count=view_count,
                    comment_count=comment_count,
                    is_answered=question.get('is_answered'),
                    accepted_answer_id=question.get('accepted_answer_id'),
                    tags=tags_str,
                    owner_user_id=question.get('owner', {}).get('user_id')
                ))

            self.db_session.commit()

            questions_retries_counter += 1

            sleep(self.COOL_DOWN_TIME)

    # Endpoint URL: https://api.stackexchange.com/2.3/questions/{ids}/answers
    # Docs URL: https://api.stackexchange.com/docs/answers-on-questions

    def fetch_answers_for_questions(self):
        """ The idea is to fetch all answers for all questions in the parameter question_ids_for_answers.
            Given the endpoint to fetch answers for questions has the format: questions/{ids}/answers, where ids is a ';' separated list of question ids,
            it may lead to invalid request if the list of question ids is too long - we need to split the list into a reasonably smaller chunks.
            The approach is to fetch answers for a particular window of questions (at a time)  e.g. from 0th - 9th question.
            Considering each question has several answers we need to find their count in this window which (easily from cumulative_total_answers_for_questions in the same index window).
            We divide the total count for window by 100 (max allowed page size by the API) to get the max pages to fetch for this window.  
            We fetch the answers for this window and insert them into the DB, sleep to avoid throttling and then move to the next window of questions.
            Repeat the process until we have fetched all answers for all questions.
        """

        start_q_window = 0
        end_q_window = self.TARGET_QUESTIONS_PER_PAGE
        while start_q_window < len(self.question_ids_for_answers):
            # Start from 0 if it is the first item in the list
            min_count_for_window = 0

            if start_q_window > 0:
                min_count_for_window = self.cumulative_total_answers_for_questions[
                    start_q_window - 1]

            # if remaining questions are less than window size, set the end window to the last question
            if end_q_window > len(self.question_ids_for_answers):
                end_q_window = len(self.question_ids_for_answers)

            max_count_for_window = self.cumulative_total_answers_for_questions[end_q_window - 1]

            window_count = max_count_for_window - min_count_for_window

            # Set the max pages to fetch for this window
            self.SITE.page_size = self.DEFAULT_PAGE_SIZE
            self.SITE.max_pages = math.ceil(window_count / self.SITE.page_size)

            # Use stack api to fetch the answers for this window. The library handles pagination for us and returns when all pages are fetched
            answers = self.SITE.fetch(
                'questions/{ids}/answers', ids=self.question_ids_for_answers[start_q_window:end_q_window], sort='votes', order='desc', filter='withbody')

            # Get each answer item and insert into DB
            for answer in answers['items']:
                self.db_session.add(Answer(
                    answer_id=answer.get('answer_id'),
                    question_id=answer.get('question_id'),
                    body=Utils.remove_html_tags(answer.get('body')),
                    creation_date=answer.get('creation_date'),
                    last_edit_date=answer.get('last_edit_date'),
                    last_activity_date=answer.get('last_activity_date'),
                    score=answer.get('score'),
                    is_accepted=answer.get('is_accepted'),
                    owner_user_id=answer.get('owner', {}).get('user_id')
                ))

            self.db_session.commit()

            # Move to the next window of questions
            start_q_window += self.TARGET_QUESTIONS_PER_PAGE
            end_q_window += self.TARGET_QUESTIONS_PER_PAGE

            # Ensure to cool down to avoid throttling
            sleep(self.COOL_DOWN_TIME)

    # Endpoint URL: https://api.stackexchange.com/2.3/questions/{ids}/comments
    # Docs URL: https://api.stackexchange.com/docs/comments-on-questions
    def fetch_comments_for_questions(self):
        """ We fetch all comments for all questions in the parameter question_ids_for_comments.
            Given the endpoint to fetch comments for questions has the format: questions/{ids}/comments, where ids is a ';' separated list of question ids,
            it may lead to invalid request if the list of question ids is too long - we need to split the list into a reasonably smaller chunks.
            The approach is to fetch comments for a particular window of questions (at a time)  e.g. from 0th - 9th question.
            Considering each question may have several comments we need to find their count in this window which (easily from cumulative_total_comments_for_questions in the same index window).
            We divide the total count for window by 100 (max allowed page size by the API) to get the max pages to fetch for this window.  
            We fetch the comments for this window and insert them into the DB, sleep to avoid throttling and then move to the next window of questions.
            Repeat the process until we have fetched all comments for all questions.
        """

        start_q_window = 0
        end_q_window = self.TARGET_QUESTIONS_PER_PAGE
        while start_q_window < len(self.question_ids_for_comments):
            # Start from 0 if it is the first item in the list
            min_count_for_window = 0

            if start_q_window > 0:
                min_count_for_window = self.cumulative_total_comments_for_questions[
                    start_q_window - 1]

            # if remaining questions are less than window size, set the end window to the last question
            if end_q_window > len(self.question_ids_for_comments):
                end_q_window = len(self.question_ids_for_comments)

            max_count_for_window = self.cumulative_total_comments_for_questions[end_q_window - 1]

            window_count = max_count_for_window - min_count_for_window

            # Set the max pages to fetch for this window
            self.SITE.page_size = self.DEFAULT_PAGE_SIZE
            self.SITE.max_pages = math.ceil(window_count / self.SITE.page_size)

            # Use stack api to fetch the comments for this window. The library handles pagination for us and returns when all pages are fetched
            comments = self.SITE.fetch(
                'questions/{ids}/comments', ids=self.question_ids_for_comments[start_q_window:end_q_window], sort='votes', order='desc', filter='withbody')

            # Get each comment item and insert into DB
            for comment in comments['items']:
                # Insert data
                self.db_session.add(Comment(
                    comment_id=comment.get('comment_id'),
                    post_id=comment.get('post_id'),
                    body=Utils.remove_html_tags(comment.get('body')),
                    creation_date=comment.get('creation_date'),
                    edited=comment.get('edited'),
                    score=comment.get('score'),
                    owner_user_id=comment.get('owner', {}).get('user_id'),
                    reply_to_user_user_id=comment.get(
                        'reply_to_user', {}).get('user_id')
                ))
            self.db_session.commit()

            # Move to the next window of questions
            start_q_window += self.TARGET_QUESTIONS_PER_PAGE
            end_q_window += self.TARGET_QUESTIONS_PER_PAGE

            # Ensure to cool down to avoid throttling
            sleep(self.COOL_DOWN_TIME)
