Drop table T1;
create table T1 as SELECT reporting_economy,partner_economy,sum(a2015) AS METRIC FROM WtoData_20220412181248
group by reporting_economy,partner_economy;

select * from T1

drop table if EXISTS T2;
create table T2 as select reporting_economy,partner_economy,metric,IFNULL(RANK() OVER (partition by reporting_economy ORDER BY METRIC desc),0) AS rankx from T1
where metric is not NULL
ORDER by reporting_economy;

select * from T2
where rankx < 7 and partner_economy <> 'World';
