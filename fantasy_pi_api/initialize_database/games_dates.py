import pgtoolbox as pgtb
import datetime


def create_games_dates(inception="2018-01-01 14:30:00", games_no=15):
    games_dates = []
    date_format = "%Y-%m-%d %H:%M:%S"
    game_start = datetime.datetime.strptime(inception, date_format)
    while games_no:
        game_end = game_start + datetime.timedelta(days=4, hours=6)
        game_definition = (
            datetime.datetime.strftime(game_start, date_format),
            datetime.datetime.strftime(game_end, date_format),
        )
        games_dates.append(game_definition)

        game_start = game_start + datetime.timedelta(days=7)
        games_no = games_no - 1

    return games_dates


def upload_games_dates():

    games_dates = create_games_dates(inception="2019-12-30 14:30:00", games_no=15)
    print(games_dates)
    db_con = pgtb.db_toolbox.connect_to_database()
    db_con.execute_query('truncate fantasy_pi_schema.games_dates restart identity cascade')
    db_con.multiple_insert(
        "fantasy_pi_schema",
        "games_dates",
        ["game_start", "game_end"],
        games_dates,
    )
    db_con.commit_changes()


if __name__ == "__main__":
    upload_games_dates()
