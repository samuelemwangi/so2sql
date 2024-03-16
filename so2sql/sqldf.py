import pandas as pd

from sqlalchemy import literal, union_all

from .models import Question, Answer, Comment

class SqlDf:
    def __init__(self, db_session):
        self.db_session = db_session

    def check_missing_values(self, df):
        total = df.isnull().sum().sort_values(ascending=False)
        percent = (df.isnull().sum() / df.isnull().count()
                   * 100).sort_values(ascending=False)
        missing_values = pd.concat(
            [total, percent], axis=1, keys=['Total', 'Percent'])
        return missing_values
    
    def get_combined_text_df(self, df):
        question_titles = self.db_session.query(
            Question.question_id.label('item_id'),
            Question.title.label('item_text'),
            literal('question').label('item_type'),
            literal('title').label('title_or_body'),
            Question.creation_date.label('creation_date'),
            Question.last_edit_date.label('last_edit_date'),
            Question.last_activity_date.label('last_activity_date')
        )

        question_bodies = self.db_session.query(
            Question.question_id.label('item_id'),
            Question.body.label('item_text'),
            literal('question').label('item_type'),
            literal('body').label('title_or_body'),
            Question.creation_date.label('creation_date'),
            Question.last_edit_date.label('last_edit_date'),
            Question.last_activity_date.label('last_activity_date')
        )

        answer_bodies = self.db_session.query(
            Answer.answer_id.label('item_id'),
            Answer.body.label('item_text'),
            literal('answer').label('item_type'),
            literal('body').label('title_or_body'),
            Answer.creation_date.label('creation_date'),
            Answer.last_edit_date.label('last_edit_date'),
            Answer.last_activity_date.label('last_activity_date')
        )

        comment_bodies = self.db_session.query(
            Comment.comment_id.label('item_id'),
            Comment.body.label('item_text'),
            literal('comment').label('item_type'),
            literal('body').label('title_or_body'),
            Comment.creation_date.label('creation_date'),
            literal(None).label('last_edit_date'),
            literal(None).label('last_activity_date')
        )
        # Union all the subqueries
        combined_query = union_all(question_titles, question_bodies, answer_bodies, comment_bodies)

        # Create a dataframe for the combined text
        combined_text_df = pd.read_sql_query(combined_query, self.db_session.bind)

        return combined_text_df
