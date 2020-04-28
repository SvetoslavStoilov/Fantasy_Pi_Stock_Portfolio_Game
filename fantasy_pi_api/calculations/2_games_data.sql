drop table if exists fantasy_pi_schema.games_data;
create table fantasy_pi_schema.games_data as
    select 
        ap.game_id
        ,g.game_name
        ,g.game_fee
        ,g.game_start
        ,g.game_end
        ,g.game_type
        ,g.is_public
        ,ap.user_id
        ,u.email
        ,ap.portfolio_id
        ,pf.portfolio_name
        ,ap.ticker
        ,ap.percentage_invested
        ,ar.return_per_company
        ,r.portfolio_return

    from fantasy_pi_schema.aggregated_prices ap
    join fantasy_pi_schema.aggregated_results ar 
        on ap.game_id = ar.game_id
        and ap.user_id = ar.user_id
        and ap.portfolio_id = ar.portfolio_id
        and ap.ticker = ar.ticker
    join fantasy_pi_schema.games g
        on ap.game_id = g.game_id
    join fantasy_pi_schema.users u
        on ap.user_id = u.user_id
    join fantasy_pi_schema.portfolios pf
        on ap.portfolio_id = pf.portfolio_id
    join fantasy_pi_schema.results r
        on ap.game_id = r.game_id
        and ap.user_id = r.user_id
        and ap.portfolio_id = r.portfolio_id;
