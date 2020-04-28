drop table if exists fantasy_pi_schema.aggregated_prices;
create table fantasy_pi_schema.aggregated_prices as
select
  pfbd.game_id
  ,pfbd.user_id
  ,pfbd.portfolio_id
  ,pfbd.ticker
  ,mindate.mindate as price_open_ts
  ,pr1.opening
  ,maxdate.maxdate as price_closing_ts
  ,pr2.closing
  ,pfbd.percentage_invested

from fantasy_pi_schema.portfolios_breakdown pfbd
join fantasy_pi_schema.games gm
  on pfbd.game_id = gm.game_id


join fantasy_pi_schema.prices pr1
  on pfbd.ticker = pr1.ticker
join (
  select 
    ticker
    ,date(timestamp) as date
    ,min(timestamp) as mindate

  from fantasy_pi_schema.prices
  group by 1,2
) mindate
  on pr1.ticker = mindate.ticker
  and pr1.timestamp = mindate.mindate
  and date(gm.game_start) = mindate.date


join fantasy_pi_schema.prices pr2
  on pfbd.ticker = pr2.ticker
join (
  select 
    ticker
    ,date(timestamp) as date
    ,max(timestamp) as maxdate

  from fantasy_pi_schema.prices
  group by 1,2
) maxdate
  on pr2.ticker = maxdate.ticker
  and pr2.timestamp = maxdate.maxdate
  and date(gm.game_end) = maxdate.date
group by 1,2,3,4,5,6,7,8,9
order by 1,2,3,4;


drop table if exists fantasy_pi_schema.aggregated_results;
create table fantasy_pi_schema.aggregated_results as
select
  ap.game_id
  ,ap.user_id
  ,ap.portfolio_id
  ,ap.ticker
  ,ap.percentage_invested :: float / 100 * ( (ap.closing - ap.opening) / ap.opening  ) as return_per_company
from fantasy_pi_schema.aggregated_prices ap;


drop table if exists fantasy_pi_schema.results;
create table fantasy_pi_schema.results as
  select 
    ar.game_id game_id
    ,ar.user_id user_id
    ,ar.portfolio_id portfolio_id
    ,AVG(ar.return_per_company) portfolio_return
  from fantasy_pi_schema.aggregated_results ar
  group by 1,2,3
  order by 4 DESC;
