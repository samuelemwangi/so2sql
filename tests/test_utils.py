from unittest import TestCase

from so2sql.utils import Utils

class TestUtils(TestCase):
    def test_remove_html_tags(self):
        sample_html = "<div><p>Some text</p><code><html><body>Hello</body></html><</code></div>"
        actual = Utils.remove_html_tags(sample_html)
        expected = "Some text"
        self.assertEqual(actual, expected)

    def test_convert_date_time_to_unix_timestamp(self):
        sample_date = "15-03-2020"
        actual = Utils.convert_date_time_to_unix_timestamp(sample_date)
        expected = 1584219600
        self.assertEqual(actual, expected)

    def test_resolve_date_day(self):
        sample_date = 1584219600
        actual = Utils.resolve_date_day(sample_date)
        expected = "Sunday"
        self.assertEqual(actual, expected)

    def test_resolve_date_month(self):
        sample_date = 1584219600
        actual = Utils.resolve_date_month(sample_date)
        expected = "March"
        self.assertEqual(actual, expected)

    def test_resolve_actual_date_of_the_month(self):
        sample_date = 1584219600
        actual = Utils.resolve_actual_date_of_the_month(sample_date)
        expected = "15"
        self.assertEqual(actual, expected)

    def test_resolve_actual_date(self):
        sample_date = 1584219600
        actual = Utils.resolve_actual_date(sample_date)
        expected = "2020-03-15 00:00:00"
        self.assertEqual(str(actual), expected)
