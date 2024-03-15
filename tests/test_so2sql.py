import json

from unittest import TestCase
from unittest.mock import MagicMock

from so2sql import So2Sql


from .mockresponses import question_data, answers_data, comments_data


class TestSo2Sql(TestCase):

    def test_fetch_questions_data(self):    
        db_session = MagicMock()

        so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)
        so_2_sql.SITE.fetch = MagicMock(return_value=question_data)
        so_2_sql.db_session.add = MagicMock()
        so_2_sql.db_session.commit = MagicMock()

        so_2_sql.fetch_questions_data()

        self.assertEqual(so_2_sql.question_ids_for_answers, [78168946, 78168947])        
        self.assertEqual(so_2_sql.cumulative_total_answers_for_questions, [1,3])

        self.assertEqual(so_2_sql.question_ids_for_comments,[78168947])        
        self.assertEqual(so_2_sql.cumulative_total_comments_for_questions, [1])

        self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
        self.assertEqual(so_2_sql.db_session.add.call_count, 2)
        self.assertEqual(so_2_sql.db_session.commit.call_count, 1)

    def test_fetch_answers_for_questions(self):
        db_session = MagicMock()

        so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)
        so_2_sql.SITE.fetch = MagicMock(return_value=answers_data)
        so_2_sql.db_session.add = MagicMock()
        so_2_sql.db_session.commit = MagicMock()

        so_2_sql.question_ids_for_answers = [78169423,78169598]
        so_2_sql.cumulative_total_answers_for_questions = [1,2]

        so_2_sql.fetch_answers_for_questions()

        self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
        self.assertEqual(so_2_sql.db_session.add.call_count, 3)
        self.assertEqual(so_2_sql.db_session.commit.call_count, 1)

    def test_fetch_comments_for_questions(self):
        db_session = MagicMock()

        so_2_sql = So2Sql(db_session=db_session, cool_down_time=0)
        so_2_sql.SITE.fetch = MagicMock(return_value=comments_data)
        so_2_sql.db_session.add = MagicMock()
        so_2_sql.db_session.commit = MagicMock()

        so_2_sql.question_ids_for_comments = [78169598]
        so_2_sql.cumulative_total_comments_for_questions = [2]

        so_2_sql.fetch_comments_for_questions()

        self.assertEqual(so_2_sql.SITE.fetch.call_count, 1)
        self.assertEqual(so_2_sql.db_session.add.call_count, 2)
        self.assertEqual(so_2_sql.db_session.commit.call_count, 1)
        
