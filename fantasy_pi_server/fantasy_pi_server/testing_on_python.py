@data.route("/add_portfolio", methods=["POST"])
@authenticc.login_user
def add_portfolio():
    if authenticc.get_user_data().get("is_authenticated"):
        user_id = authenticc.get_user_data()["user_id"]
        portfolio_name = request.headers.get("portfolio_name")
        game_id = request.headers.get("game_id")
        db_con = pgtb.connect_to_database()
        qr = f"""
            insert into fantasy_pi_schema.portfolios(portfolio_name, user_id, game_id) values ('{portfolio_name}', '{user_id}', '{game_id}') """
        db_con.execute_query(qr)
        db_con.commit_changes()

        qr = f"""
            select *
            from fantasy_pi_schema.portfolios
            where portfolio_name = '{portfolio_name}'
                and user_id = '{user_id}'
                and game_id = '{game_id}'
        """
        result = db_con.read_query(qr)
        return jsonify(result)


@data.route("/delete_portfolio", methods=["POST", "PUT"])
@authenticc.login_user
def delete_portfolio():
    if authenticc.get_user_data().get("is_authenticated"):
        user_id = authenticc.get_user_data()["user_id"]
        portfolio_name = request.headers.get("portfolio_name")
        game_id = request.headers.get("game_id")
        db_con = pgtb.connect_to_database()
        qr = f"""
            delete from fantasy_pi_schema.portfolios 
                where 
                portfolio_name = '{portfolio_name}'
                AND user_id = '{user_id}'
                AND game_id = '{game_id}' """

        db_con.execute_query(qr)
        db_con.commit_changes()

        return jsonify(qr)