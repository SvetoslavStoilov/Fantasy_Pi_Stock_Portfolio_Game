import pgtoolbox as pgtb
import os
import argparse


def upload_data(path="./insert_test_data/test_data/"):

    db_con = pgtb.db_toolbox.connect_to_database()

    sql_scripts = os.listdir(path)
    sql_scripts.sort()
    sql_scripts = [path + script for script in sql_scripts]

    for script in sql_scripts:
        print(script)
        queries_runner = pgtb.db_toolbox.QueriesRunner(db_con, script)
        queries_runner.read_queries()
        queries_runner.run_queries()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run all the sql scripts inside a folder"
    )
    parser.add_argument(
        "-p", action="store", dest="path", help="The path to the sql scripts folder",
    )

    path = parser.parse_args().path

    upload_data(path)
