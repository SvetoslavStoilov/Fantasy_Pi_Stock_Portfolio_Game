import api_base
import requests
import datetime
import time
import sys


def test_api(start=None, end=None):
    start = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')

    tickers = ["AAPL", "MSFT", "GOOG", "TSLA", "WMT"]
    # tickers = ["AAPL", "MSFT"]


    for ticker in tickers:
        company = api_base.YhFinanceApi(ticker)
        data = company.get_data(interval="1h", start="2020-01-06", end="2020-01-11")
        timestamps = data.json()["chart"]["result"][0]["timestamp"]
        timestamps = list(map(lambda x: api_base.convert_to_date(x), timestamps))
        opening_prices = data.json()["chart"]["result"][0]["indicators"]["quote"][0][
            "open"
        ]
        closing_prices = data.json()["chart"]["result"][0]["indicators"]["quote"][0][
            "close"
        ]
        ticker_ls = [ticker for i in range(len(timestamps))]

        print("ticker_ls is: ", ticker_ls)
        print("timestamps is: ", timestamps)
        print("opening_prices is: ", opening_prices)
        print("closing_prices is: ", closing_prices)

if __name__ == '__main__':
    test_api()
