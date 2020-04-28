import os
import requests
import datetime
import time
import sys
import pgtoolbox as pgtb


def get_database_config():
    return {
        "db_host": os.environ["FANTASY_PI_DB_HOST"],
        "db_name": os.environ["FANTASY_PI_DB_NAME"],
        "db_user": os.environ["FANTASY_PI_DB_USER"],
        "db_pass": os.environ["FANTASY_PI_DB_PORT"],
        "db_port": os.environ["FANTASY_PI_DB_PASS"],
    }


class YhFinanceApi:
    def __init__(self, ticker):
        self._ticker = ticker.upper()
        self._base_url = "https://query1.finance.yahoo.com"

    def get_data(self, start=None, end=None, interval="1d"):
        def convert_date_to_unixtime(input_time):
            print("input time is: ", input_time)
            if isinstance(input_time, datetime.datetime):
                output_time = int(time.mktime(input_time.timetuple()))
            if isinstance(input_time, str):
                output_time = datetime.datetime.strptime(
                    input_time, "%Y-%m-%d %H:%M:%S"
                )
                output_time = int(time.mktime(output_time.timetuple()))
            return output_time

        url = "{}/v8/finance/chart/{}".format(self._base_url, self._ticker)

        if start is None and end is None:
            start = int(time.time())
            end = int(time.time())
        elif start and end is None:
            start = convert_date_to_unixtime(start)
            end = int(time.time())
        elif start is None and end:
            start = -2208988800
            end = convert_date_to_unixtime(end)
        elif start and end:
            start = convert_date_to_unixtime(start)
            end = convert_date_to_unixtime(end)
        else:
            print("Something is wrong with the format of the dates requested.")
            sys.exit()

        params = {"period1": start, "period2": end}
        params["symbol"] = self._ticker
        params["interval"] = interval

        data = requests.get(url=url, params=params)

        return data


def convert_to_date(timest):
    date = datetime.datetime.fromtimestamp(timest)
    date = date.strftime("%Y-%m-%d %H:%M:%S")

    return date


def get_api_data(ticker, start, end, interval="1d"):
    company = YhFinanceApi(ticker)
    data = company.get_data(start, end, interval)

    return data


def push_to_db(data, db_con):
    print("Pushing into the db.")

    timestamps = data.json()["chart"]["result"][0]["timestamp"]
    ticker = data.json()["chart"]["result"][0]["meta"]["symbol"]
    timestamps = list(map(lambda x: convert_to_date(x), timestamps))
    opening_prices = data.json()["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    closing_prices = data.json()["chart"]["result"][0]["indicators"]["quote"][0][
        "close"
    ]
    ticker_ls = [ticker for i in range(len(timestamps))]

    prices_table_tup = db_con.transform_data_for_insert(
        ticker_ls, timestamps, opening_prices, closing_prices
    )

    db_con.multiple_insert(
        "fantasy_pi_schema",
        "prices",
        ["ticker", "timestamp", "closing", "opening"],
        prices_table_tup,
    )
    db_con.commit_changes()


def get_ticker_data():
    start = None
    end = None
    # start = "2019-12-30 14:30:00"
    # end = "2020-01-10 20:30:00"

    db_con = pgtb.db_toolbox.connect_to_database()

    tickers = db_con.read_query(
        "select ticker from fantasy_pi_schema.portfolios_breakdown group by ticker"
    )
    tickers = [el[0] for el in tickers]
    print(f"tickers to get data for are: {tickers}")

    for ticker in tickers:
        retries = 3
        ok = False
        while retries and not ok:
            data = get_api_data(ticker, start, end, interval="1d")
            data_json = data.json()
            if (
                "chart" in dict.keys(data_json)
                and "result" in dict.keys(data_json["chart"])
                and "timestamp" in dict.keys(data_json["chart"]["result"][0])
            ):
                push_to_db(data, db_con)
                ok = True
            else:
                print(
                    f"Sleeping for 10 seconds because failed to get the data initially. Retries left number: {retries - 1}"
                )
                time.sleep(10)
        if ok == False:
            print(f"Failed to get data for company {ticker}.")


if __name__ == "__main__":
    get_ticker_data()
