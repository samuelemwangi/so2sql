import pandas as pd


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