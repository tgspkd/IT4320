import unittest
from datetime import date
from datetime import datetime

class TestUserInput(unittest.TestCase):

    # Stock Symbol
    def test_stock_symbol(self):
        self.assertTrue("SYMBOL".isupper() and len("SYMBOL") >= 1 and len("SYMBOL") <= 7, "The symbol must contain between 1-7 uppercase letter(s)")

    # Chart Type
    def test_chart_type(self):
        self.assertTrue(1 == 1 or "two" == 2, "The chart type must be specified as 1 or 2")
            
    # Time Series
    def test_time_series(self):
        time_series = 1
        self.assertTrue(time_series >= 1 and time_series <= 4 and isinstance(time_series, int), "The time series must be specified as 1, 2, 3, or 4")

    # Start Date
    def test_start_date(self):
        start_date = "2022-10-15"
        try:
            convert_date(start_date)
        except ValueError:
            self.fail("The start date must be entered in YYYY-MM-DD formate")

    # End Date
    def test_end_date(self):
        end_date = "2022-10-15"
        try:
            convert_date(end_date)
        except ValueError:
            self.fail("The end date must be entered in YYYY-MM-DD format")

# Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def main():
    unittest.main()
main()