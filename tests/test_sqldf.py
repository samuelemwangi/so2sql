from unittest import TestCase

import pandas as pd
import numpy as np

from sqlalchemy import literal, union_all

from unittest.mock import patch, MagicMock

from so2sql import SqlDf, Question

class TestSqlDF(TestCase):
    def test_check_missing_values(self):
        df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [np.nan, 2, 3, 4, 5],
            'C': [1, 2, 3, 4, np.nan]
        })

        db_session = MagicMock()
        sql_df = SqlDf(db_session=db_session)

        result = sql_df.check_missing_values(df)

        expected_result = pd.DataFrame({
            'Total': [1, 1, 1],
            'Percent': [20.0, 20.0, 20.0]
        }, index=['A', 'B', 'C']).sort_values(by='Total', ascending=False)

        pd.testing.assert_frame_equal(result, expected_result)
