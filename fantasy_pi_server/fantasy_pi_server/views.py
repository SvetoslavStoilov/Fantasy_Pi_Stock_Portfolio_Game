from flask import Blueprint, jsonify, request
from pgtoolbox import db_toolbox as pgtb

from decimal import Decimal
import datetime
from operator import itemgetter
import json

from fantasy_pi_server.authenticc import Authenticc

data = Blueprint("data", __name__)
authenticc = Authenticc()


@data.route("/games_data_all", endpoint="get_games_data_all")
@authenticc.login_user
def get_games_data_all():
    def make_json(games_data):
        def make_game_object(game, row):
            game["game_id"] = row[0]
            game["game_name"] = row[1]
            game["game_fee"] = int(row[2])
            game["game_start"] = row[3].strftime("%Y-%m-%d %H:%M:%S")
            game["game_end"] = row[4].strftime("%Y-%m-%d %H:%M:%S")
            game["game_type"] = row[5]
            game["is_public"] = row[6]
            portfolios_data_item = {
                "user_id": row[7],
                "email": row[8],
                "portfolio_id": row[9],
                "portfolio_name": row[10],
                "company": row[11],
                "percentage_invested": row[12],
                "return_per_company": row[13],
                "portfolio_return": row[14],
            }
            if "portfolios_data" not in dict.keys(game):
                game["portfolios_data"] = [portfolios_data_item]
            else:
                game["portfolios_data"].append(portfolios_data_item)

            return game

        games_data = sorted(games_data, key=itemgetter(1))
        result = []
        game = {}
        for row in games_data:
            current_game_id = row[0]
            if not game or (
                "game_id" in dict.keys(game) and game["game_id"] == current_game_id
            ):
                game = make_game_object(game, row)
            else:
                result.append(game)
                game = {}
                game = make_game_object(game, row)
        result.append(game)

        # result = json.dumps(result)
        return result

    # user_credentials = authenticc.get_user_credentials()
    db_con = pgtb.connect_to_database()
    games_data = db_con.read_query(
        """select 
                game_id, 
                game_name, 
                game_fee, 
                game_start, 
                game_end, 
                game_type, 
                is_public, 
                user_id, 
                email, 
                portfolio_id, 
                portfolio_name, 
                ticker, 
                percentage_invested, 
                return_per_company, 
                portfolio_return 
            from fantasy_pi_schema.games_data
        """
    )

    games_data_json = make_json(games_data)

    registered_companies = [
        {
            "game_id": game["game_id"],
            "registered_companies": list(
                set(
                    map(
                        itemgetter(1),
                        db_con.read_query(
                            f"select game_id, ticker from fantasy_pi_schema.portfolios_breakdown where game_id = {game['game_id']}"
                        ),
                    )
                )
            ),
        }
        for game in games_data_json
    ]
    registered_users = [
        {
            "game_id": game["game_id"],
            "registered_users": list(
                set(
                    map(
                        itemgetter(0),
                        db_con.read_query(
                            f"""select u.email 
                            from 
                            fantasy_pi_schema.portfolios_breakdown pb
                            join fantasy_pi_schema.users u
                             
                            on u.user_id = pb.user_id

                            where game_id = {game['game_id']}"""
                        ),
                    )
                )
            ),
        }
        for game in games_data_json
    ]
    for game in games_data_json:
        game_id = game["game_id"]
        for item in registered_users:
            if game_id == item["game_id"]:
                game["registered_users"] = item["registered_users"]
        for item in registered_companies:
            if game_id == item["game_id"]:
                game["registered_companies"] = item["registered_companies"]

    games_data_json = {"results": games_data_json}

    return jsonify(games_data_json)


@data.route("/games_data", endpoint="get_games_data")
@authenticc.login_user
def get_games_data():
    def make_json(games_data):
        def make_game_object(game, row):
            game["game_id"] = row[0]
            game["game_name"] = row[1]
            game["game_fee"] = int(row[2])
            game["game_start"] = row[3].strftime("%Y-%m-%d %H:%M:%S")
            game["game_end"] = row[4].strftime("%Y-%m-%d %H:%M:%S")
            game["game_type"] = row[5]
            game["is_public"] = row[6]

            return game

        result = []
        for row in games_data:
            game = {}
            game = make_game_object(game, row)
            result.append(game)

        return result

    user_credentials = authenticc.get_user_credentials()
    if not user_credentials.get("is_authenticated"):
        # TODO return an error instead
        return jsonify({})
    user_id = user_credentials.get("user_id")
    game_id = request.args.get("game_id")
    where_statement_games_data = f"where user_id = {user_id}"
    where_statement_games_data = (
        f"{where_statement_games_data} and game_id = {game_id}"
        if game_id is not None
        else where_statement_games_data
    )
    where_statement_results = (
        f"where rs.game_id = {game_id}" if game_id is not None else ""
    )

    db_con = pgtb.connect_to_database()
    games_data = db_con.read_query(
        f"""select 
                game_id, 
                game_name, 
                game_fee, 
                game_start, 
                game_end, 
                game_type, 
                is_public
            from fantasy_pi_schema.games_data
            {where_statement_games_data}
            group by 1,2,3,4,5,6,7
        """
    )
    games_data_json = make_json(games_data)

    registered_companies = [
        {
            "game_id": game["game_id"],
            "registered_companies": list(
                set(
                    map(
                        itemgetter(1),
                        db_con.read_query(
                            f"select game_id, ticker from fantasy_pi_schema.portfolios_breakdown where game_id = {game['game_id']}"
                        ),
                    )
                )
            ),
        }
        for game in games_data_json
    ]
    results = db_con.read_query(
        f""" 
        select 
            rs.game_id,
            rs.user_id,
            rs.portfolio_id,
            rs.portfolio_return,
            pf.portfolio_name, 
            array_agg(pbd.ticker) as tickers,
            array_agg(pbd.percentage_invested) as percentages
        from fantasy_pi_schema.results rs 
        join fantasy_pi_schema.portfolios pf 
            on rs.portfolio_id = pf.portfolio_id 
        join fantasy_pi_schema.portfolios_breakdown pbd
            on pf.portfolio_id = pbd.portfolio_id
        join fantasy_pi_schema.users u
            on u.user_id = {user_id}
        {where_statement_results}
        group by 1,2,3,4,5
        order by 1,4 desc 
        """
    )
    rankings = []
    current_game = results[0][0]
    obj = {}
    for row in results:
        if row[0] == current_game:
            if not obj:
                obj = {
                    "game_id": row[0],
                    "rankings": [
                        [
                            row[4],
                            row[3],
                            [
                                {"company": row[5][i], "percentage_invested": row[6][i]}
                                for i in range(len(row[5]))
                            ],
                        ],
                    ],
                }
            else:
                obj["rankings"].append(
                    [
                        row[4],
                        row[3],
                        [
                            [
                                {"company": row[5][i], "percentage_invested": row[6][i]}
                                for i in range(len(row[5]))
                            ],
                        ],
                    ]
                )
        else:
            current_game = row[0]
            rankings.append(obj)
            obj = {
                "game_id": row[0],
                "rankings": [
                    [
                        row[4],
                        row[3],
                        [
                            {"company": row[5][i], "percentage_invested": row[6][i]}
                            for i in range(len(row[5]))
                        ],
                    ],
                ],
            }
    rankings.append(obj)

    for game in games_data_json:
        game_id = game["game_id"]
        for item in registered_companies:
            if game_id == item["game_id"]:
                game["registered_companies"] = item["registered_companies"]
        for item in rankings:
            if game_id == item["game_id"]:
                game["rankings"] = item["rankings"]

    games_data_json = {"results": games_data_json}

    return jsonify(games_data_json)


portfolios = Blueprint("portfolios", __name__)


@portfolios.route("/add_portfolio", methods=["POST"], endpoint="add_portfolio")
@authenticc.login_user
def add_portfolio():
    user_id = authenticc.get_user_credentials().get("user_id")
    if user_id:
        portfolio_name = request.headers.get("portfolio_name")
        game_id = request.headers.get("game_id")
        db_con = pgtb.connect_to_database()
        qr = f"""
            insert into fantasy_pi_schema.portfolios(portfolio_name, user_id, game_id) values ('{portfolio_name}', '{user_id}', '{game_id}') """
        db_con.execute_query(qr)
        db_con.commit_changes()

        qr = f"""
            select user_id, game_id, portfolio_id, portfolio_name
            from fantasy_pi_schema.portfolios
            where portfolio_name = '{portfolio_name}'
                and user_id = '{user_id}'
                and game_id = '{game_id}'
        """
        query_read = db_con.read_query(qr)
        result = {
            "user_id": query_read[0][0],
            "game_id": query_read[0][1],
            "portfolio_id": query_read[0][2],
            "portfolio_name": query_read[0][3],
        }
        return jsonify(result)
    else:
        # TODO error codes
        return jsonify({})

@data.route("/delta_data", endpoint="delta_data")
# @authenticc.login_user
def delta_data():
    db_con = pgtb.connect_to_database()
    delta_data = db_con.read_query('''SELECT * FROM fantasy_pi_schema.delta_prices''')
    data = [{'company': delta_data[i][0], 'delta2': delta_data[i][1], 'delta4': delta_data[i][2], 'delta6': delta_data[i][3], 'timestamp': delta_data[i][4]} for i in range(len(delta_data))]
    return jsonify(data)

@portfolios.route("/add_company", methods=["POST"], endpoint="add_company")
@authenticc.login_user
def add_company():

    user_id = authenticc.get_user_credentials()["user_id"]
    if user_id:
        game_id = request.headers.get("game_id")
        portfolio_id = request.headers.get("portfolio_id")
        ticker = request.headers.get("ticker")
        percentage_invested = request.headers.get("percentage_invested")

        db_con = pgtb.connect_to_database()
        qr = f"""
            insert into fantasy_pi_schema.portfolios_breakdown
            (game_id, user_id, portfolio_id, ticker, percentage_invested) 
            values 
            ('{game_id}', '{user_id}', '{portfolio_id}', '{ticker}', '{percentage_invested}') """

        db_con.execute_query(qr)
        db_con.commit_changes()

        qr = f"""
            select game_id, user_id, portfolio_id, ticker, percentage_invested
            from fantasy_pi_schema.portfolios_breakdown
            where game_id = '{game_id}'
                and user_id = '{user_id}'
                and portfolio_id = '{portfolio_id}'
                and ticker = '{ticker}'
                and percentage_invested = '{percentage_invested}'
        """
        query_read = db_con.read_query(qr)
        result = {
            "game_id": query_read[0][0],
            "user_id": query_read[0][1],
            "portfolio_id": query_read[0][2],
            "ticker": query_read[0][3],
            "percentage_invested": query_read[0][4],
        }
        return jsonify(result)
    else:
        # TODO error codes
        return jsonify({})


@portfolios.route(
    "/delete_portfolio", methods=["POST", "PUT"], endpoint="delete_portfolio"
)
@authenticc.login_user
def delete_portfolio():
    user_id = authenticc.get_user_credentials()["user_id"]
    if user_id:
        portfolio_name = request.headers.get("portfolio_name")
        game_id = request.headers.get("game_id")
        db_con = pgtb.connect_to_database()
        qr = f"""
            delete from fantasy_pi_schema.portfolios 
                where 
                portfolio_name = '{portfolio_name}'
                AND user_id = {user_id}
                AND game_id = {game_id}
            """

        db_con.execute_query(qr)
        db_con.commit_changes()

        return jsonify({"deleted": True})
    else:
        # TODO error codes
        return jsonify({})


@portfolios.route("/delete_company", methods=["POST", "PUT"], endpoint="delete_company")
@authenticc.login_user
def delete_company():
    user_id = authenticc.get_user_credentials()["user_id"]
    if user_id:
        game_id = request.headers.get("game_id")
        portfolio_id = request.headers.get("portfolio_id")
        ticker = request.headers.get("ticker")

        db_con = pgtb.connect_to_database()
        qr = f"""
            delete from fantasy_pi_schema.portfolios_breakdown
            where game_id = {game_id}
                and user_id = {user_id}
                and portfolio_id = {portfolio_id}
                and ticker = '{ticker}'
                """

        db_con.execute_query(qr)
        db_con.commit_changes()

        return jsonify({"deleted": True})
    else:
        # TODO error codes
        return jsonify({})
