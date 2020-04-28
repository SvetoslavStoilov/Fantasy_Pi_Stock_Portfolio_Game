#!/bin/bash
#When you put this in a container you can get the env vars from docker compose
export FANTASY_PI_DB_HOST=localhost
export FANTASY_PI_DB_NAME=fantasy_pi
export FANTASY_PI_DB_USER=postgres
export FANTASY_PI_DB_PORT=5433
export FANTASY_PI_DB_PASS=''

echo "Creating the games_dates."
python3 ./initialize_database/games_dates.py
echo "Inserting the test data"
python3 ./run_sql.py -p './insert_test_data/test_data/'

