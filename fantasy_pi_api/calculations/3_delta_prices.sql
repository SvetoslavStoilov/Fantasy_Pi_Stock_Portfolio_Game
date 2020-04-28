drop table if exists fantasy_pi_schema.delta_prices;
create table fantasy_pi_schema.delta_prices as
WITH delta2 as (With temp_prices as (select 
pr1.ticker
,pr1.closing closing_1
,pr2.closing closing_2
,pr1.opening opening_1
,pr2.opening opening_2
,pr1.timestamp as start_period
,pr2.timestamp as end_period
from fantasy_pi_schema.prices pr1
join fantasy_pi_schema.prices pr2
on pr2.timestamp::date - pr1.timestamp::date = 2
and pr2.ticker = pr1.ticker)

SELECT t.ticker,t.opening_1 as Opening, t.closing_2 as Closing, r.MaxTime as period_end, (((t.closing_2 - t.opening_1)/t.opening_1)*100) as delta2
FROM (
      SELECT ticker, MAX(end_period) as MaxTime
      FROM temp_prices
      GROUP BY ticker
) r
INNER JOIN temp_prices t
ON t.ticker = r.ticker AND t.end_period = r.MaxTime),

delta4 as (With temp_prices as (select 
pr1.ticker
,pr1.closing closing_1
,pr2.closing closing_2
,pr1.opening opening_1
,pr2.opening opening_2
,pr1.timestamp as start_period
,pr2.timestamp as end_period
from fantasy_pi_schema.prices pr1
join fantasy_pi_schema.prices pr2
on pr2.timestamp::date - pr1.timestamp::date = 4
and pr2.ticker = pr1.ticker)

SELECT t.ticker,t.opening_1 as Opening, t.closing_2 as Closing, r.MaxTime as period_end, (((t.closing_2 - t.opening_1)/t.opening_1)*100) as delta4
FROM (
      SELECT ticker, MAX(end_period) as MaxTime
      FROM temp_prices
      GROUP BY ticker
) r
INNER JOIN temp_prices t
ON t.ticker = r.ticker AND t.end_period = r.MaxTime),

delta6 as (With temp_prices as (select 
pr1.ticker
,pr1.closing closing_1
,pr2.closing closing_2
,pr1.opening opening_1
,pr2.opening opening_2
,pr1.timestamp as start_period
,pr2.timestamp as end_period
from fantasy_pi_schema.prices pr1
join fantasy_pi_schema.prices pr2
on pr2.timestamp::date - pr1.timestamp::date = 6
and pr2.ticker = pr1.ticker)

SELECT t.ticker,t.opening_1 as Opening, t.closing_2 as Closing, r.MaxTime as period_end, (((t.closing_2 - t.opening_1)/t.opening_1)*100) as delta6
FROM (
      SELECT ticker, MAX(end_period) as MaxTime
      FROM temp_prices
      GROUP BY ticker
) r
INNER JOIN temp_prices t
ON t.ticker = r.ticker AND t.end_period = r.MaxTime)

SELECT d2.ticker, d2.delta2, d4.delta4, d6.delta6, d6.period_end FROM delta2 d2
JOIN delta4 d4 ON d2.ticker = d4.ticker
JOIN delta6 d6 ON d2.ticker = d6.ticker;