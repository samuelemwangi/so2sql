import re

from datetime import datetime

from bs4 import BeautifulSoup

from numpy import isnan as np_isnan


class Utils:
    @staticmethod
    def clean_html_text(text):
        # Remove all content between <code> tags
        text = re.sub('<code>(.*?)</code>', '', str(text), flags=re.DOTALL)
        
        # Remove all content between <blockquote> tags
        text = re.sub('<blockquote>(.*?)</blockquote>', '', str(text), flags=re.DOTALL)

        # Remove other HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()
        
        # Replace any number of consecutive newline characters with a period and a space
        text = re.sub(r'\n+', '. ', str(text), flags=re.DOTALL)

        # Replace any number of consecutive space characters with a single space
        text = re.sub(r'\s+', ' ', str(text), flags=re.DOTALL)

        # Replace any number of consecutive . characters with a single .
        text = re.sub(r'\.+', '.', str(text), flags=re.DOTALL)

        # Remove leading periods
        text = re.sub(r'^\.', '', str(text), flags=re.DOTALL)

        # Remove leading and trailing spaces
        text = text.strip()

        return text

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
