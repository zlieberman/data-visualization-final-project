drop table if EXISTS T2;
create table T2 as select reporting_economy,partner_economy,year,value,IFNULL(RANK() OVER (partition by reporting_economy,year ORDER BY value desc),0) AS rankx from petroleum
where value is not NULL and partner_economy <> 'World'
ORDER by reporting_economy;

select * from T2
where rankx < 6 and year in (2000,2005,2010,2015,2020);