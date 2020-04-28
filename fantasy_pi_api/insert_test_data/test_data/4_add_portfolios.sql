insert into fantasy_pi_schema.portfolios ( portfolio_name, user_id, game_id) values
  ( 'MacanachePf1', 8, 0),
  ( 'SvetoslavPf1', 3, 0),
  ( 'BernardPf1', 1, 0),
  ( 'BernardPf2', 1, 0);

insert into fantasy_pi_schema.portfolios_breakdown (game_id, user_id, portfolio_id, ticker, percentage_invested) values
  ( 0, 8, 1, 'AAPL', 30),
  ( 0, 8, 1, 'MSFT', 50),
  ( 0, 8, 1, 'GOOG', 20),

  ( 0, 3, 2, 'GOOG', 25),
  ( 0, 3, 2, 'WMT', 25),
  ( 0, 3, 2, 'AAPL', 22),
  ( 0, 3, 2, 'TSLA', 28),

  ( 0, 1, 3, 'TSLA', 50),
  ( 0, 1, 3, 'MSFT', 50),

  ( 0, 1, 4, 'GOOG', 50),
  ( 0, 1, 4, 'MSFT', 50);

insert into fantasy_pi_schema.portfolios ( portfolio_name, user_id, game_id) values
  ( 'BernardPf3', 1, 1),
  ( 'MihneaPf1', 2, 1),
  ( 'StevePf2', 3, 1);

insert into fantasy_pi_schema.portfolios_breakdown (game_id, user_id, portfolio_id, ticker, percentage_invested) values
  ( 1, 1, 5, 'AAPL', 30),
  ( 1, 1, 5, 'MSFT', 50),
  ( 1, 1, 5, 'GOOG', 20),

  ( 1, 2, 6, 'GOOG', 25),
  ( 1, 2, 6, 'WMT', 25),
  ( 1, 2, 6, 'AAPL', 22),
  ( 1, 2, 6, 'TSLA', 28),

  ( 1, 3, 7, 'TSLA', 50),
  ( 1, 3, 7, 'MSFT', 50);

insert into fantasy_pi_schema.portfolios ( portfolio_name, user_id, game_id) values
  ( 'RaduPf1', 5, 2),
  ( 'DianaPf1', 6, 2),
  ( 'SanzianaPf1', 7, 2);

insert into fantasy_pi_schema.portfolios_breakdown (game_id, user_id, portfolio_id, ticker, percentage_invested) values
  ( 2, 5, 8, 'AAPL', 30),
  ( 2, 5, 8, 'MSFT', 50),
  ( 2, 5, 8, 'GOOG', 20),

  ( 2, 6, 9, 'GOOG', 25),
  ( 2, 6, 9, 'WMT', 25),
  ( 2, 6, 9, 'AAPL', 22),
  ( 2, 6, 9, 'TSLA', 28),

  ( 2, 7, 10, 'TSLA', 50),
  ( 2, 7, 10, 'MSFT', 50);


