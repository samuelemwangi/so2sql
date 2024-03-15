import re

from datetime import datetime

from bs4 import BeautifulSoup

from numpy import isnan as np_isnan


class Utils:
    @staticmethod
    def remove_html_tags(text):
        # Remove all content between <code> tags
        text = re.sub('<code>(.*?)</code>', '', str(text), flags=re.DOTALL)

        # Remove other HTML tags
        return BeautifulSoup(text, "html.parser").get_text()

    @staticmethod
    def convert_date_time_to_unix_timestamp(date_string):
        date = datetime.strptime(date_string, '%d-%m-%Y')
        return int(date.timestamp())

    @staticmethod
    def resolve_date_day(date):
        if date == None or np_isnan(date):
            return None
        return datetime.fromtimestamp(date).strftime('%A')

    @staticmethod
    def resolve_date_month(date):
        if date == None or np_isnan(date):
            return None
        return datetime.fromtimestamp(date).strftime('%B')

    @staticmethod
    def resolve_actual_date_of_the_month(date):
        if date == None or np_isnan(date):
            return None
        return datetime.fromtimestamp(date).strftime('%d')

    @staticmethod
    def resolve_actual_date(date):
        if date == None or np_isnan(date):
            return None
        return datetime.fromtimestamp(date)
