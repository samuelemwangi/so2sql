import json

from unittest import TestCase
from unittest.mock import patch, MagicMock

from so2sql import So2Sql, Base


from .mockresponses import question_data, answers_data, comments_data


class TestSo2Sql(TestCase):

    def test_drop_tables(self):
        db_session = MagicMock()
        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()):
            so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)

        with patch.object(Base.metadata, 'drop_all') as mock_drop_all:
            so_2_sql.drop_tables()

            mock_drop_all.assert_called_once_with(so_2_sql.db_session.bind)

    def test_create_tables(self):
        db_session = MagicMock()
        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()):
            so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)

        with patch.object(Base.metadata, 'create_all') as mock_create_all:
            so_2_sql.create_tables()

            mock_create_all.assert_called_once_with(so_2_sql.db_session.bind)

    def test_create_tables(self):
        db_session = MagicMock()
        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()):
            so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)

        with patch.object(Base.metadata, 'create_all') as mock_create_all:
            so_2_sql.create_tables()

            mock_create_all.assert_called_once_with(so_2_sql.db_session.bind)

    def test_fetch_questions_data_with_matching_count_filters(self):
        db_session = MagicMock()
        db_session.add = MagicMock()
        db_session.commit = MagicMock()

        STACK_OVERFLOW_NAMES_LOWER = ['stackoverflow']
        AI_ASSISTANT_NAMES_LOWER = ['gpt']

        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()) as mock_create_stack_api:
            so_2_sql = So2Sql(
                db_session=db_session, 
                target_questions=2, 
                questions_count_filter_1=STACK_OVERFLOW_NAMES_LOWER, 
                questions_count_filter_2=AI_ASSISTANT_NAMES_LOWER,
                cool_down_time=0
            )

            with patch.object(so_2_sql.SITE, 'fetch', return_value=question_data) as mock_fetch:
                so_2_sql.fetch_questions_data()

                self.assertEqual(so_2_sql.question_ids_for_answers, [78168946, 78168947])        
                self.assertEqual(so_2_sql.cumulative_total_answers_for_questions, [1,3])

                self.assertEqual(so_2_sql.question_ids_for_comments,[78168947])        
                self.assertEqual(so_2_sql.cumulative_total_comments_for_questions, [1])

                self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
                self.assertEqual(so_2_sql.db_session.add.call_count, 2)
                self.assertEqual(so_2_sql.db_session.commit.call_count, 1)

            mock_create_stack_api.assert_called_once()

    def test_fetch_questions_data_with_non_matching_count_filters(self):
        db_session = MagicMock()
        db_session.add = MagicMock()
        db_session.commit = MagicMock()

        STACK_OVERFLOW_NAMES_LOWER = ['testflow']
        AI_ASSISTANT_NAMES_LOWER = ['chatbot']

        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()) as mock_create_stack_api:
            so_2_sql = So2Sql(
                db_session=db_session, 
                target_questions=2, 
                questions_count_filter_1=STACK_OVERFLOW_NAMES_LOWER, 
                questions_count_filter_2=AI_ASSISTANT_NAMES_LOWER,
                cool_down_time=0
            )

            with patch.object(so_2_sql.SITE, 'fetch', return_value=question_data) as mock_fetch:
                so_2_sql.fetch_questions_data()

                self.assertEqual(so_2_sql.question_ids_for_answers, [])        
                self.assertEqual(so_2_sql.cumulative_total_answers_for_questions, [])

                self.assertEqual(so_2_sql.question_ids_for_comments,[])        
                self.assertEqual(so_2_sql.cumulative_total_comments_for_questions, [])

                self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
                self.assertEqual(so_2_sql.db_session.add.call_count, 0)
                self.assertEqual(so_2_sql.db_session.commit.call_count, 1)

            mock_create_stack_api.assert_called_once()

    def test_fetch_questions_data_with_no_count_filters(self):
        db_session = MagicMock()
        db_session.add = MagicMock()
        db_session.commit = MagicMock()

        STACK_OVERFLOW_NAMES_LOWER = []
        AI_ASSISTANT_NAMES_LOWER = []

        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()) as mock_create_stack_api:
            so_2_sql = So2Sql(
                db_session=db_session, 
                target_questions=2, 
                questions_count_filter_1=STACK_OVERFLOW_NAMES_LOWER, 
                questions_count_filter_2=AI_ASSISTANT_NAMES_LOWER,
                cool_down_time=0
            )

            with patch.object(so_2_sql.SITE, 'fetch', return_value=question_data) as mock_fetch:
                so_2_sql.fetch_questions_data()

                self.assertEqual(so_2_sql.question_ids_for_answers, [78168946, 78168947])        
                self.assertEqual(so_2_sql.cumulative_total_answers_for_questions, [1,3])

                self.assertEqual(so_2_sql.question_ids_for_comments,[78168947])        
                self.assertEqual(so_2_sql.cumulative_total_comments_for_questions, [1])

                self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
                self.assertEqual(so_2_sql.db_session.add.call_count, 2)
                self.assertEqual(so_2_sql.db_session.commit.call_count, 1)

            mock_create_stack_api.assert_called_once()    
   
    def test_fetch_answers_for_questions(self):
        db_session = MagicMock()
        db_session.add = MagicMock()
        db_session.commit = MagicMock()

        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()) as mock_create_stack_api:
            so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)
            so_2_sql.question_ids_for_answers = [78169423,78169598]
            so_2_sql.cumulative_total_answers_for_questions = [1,2]

            with patch.object(so_2_sql.SITE, 'fetch', return_value=answers_data) as mock_fetch:
                so_2_sql.fetch_answers_for_questions()

                self.assertEqual(mock_fetch.call_count, 1)
                self.assertEqual(db_session.add.call_count, 3)
                self.assertEqual(db_session.commit.call_count, 1)

            mock_create_stack_api.assert_called_once()

    def test_fetch_comments_for_questions(self):
        db_session = MagicMock()
        db_session.add = MagicMock()
        db_session.commit = MagicMock()

        with patch.object(So2Sql, 'create_stack_api', return_value=MagicMock()) as mock_create_stack_api:
            so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)
            so_2_sql.question_ids_for_comments = [78169598]
            so_2_sql.cumulative_total_comments_for_questions = [2]

            with patch.object(so_2_sql.SITE, 'fetch', return_value=comments_data) as mock_fetch:
                so_2_sql.fetch_comments_for_questions()

                self.assertEqual(mock_fetch.call_count, 1)
                self.assertEqual(db_session.add.call_count, 2)
                self.assertEqual(db_session.commit.call_count, 1)

            mock_create_stack_api.assert_called_once()