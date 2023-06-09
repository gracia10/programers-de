-- 월별 세선 수를 계산
select left(a.ts,7) as mon
     , count(1)
from raw_data.session_timestamp a
    inner join raw_data.user_session_channel b on a.sessionid = b.sessionid
group by 1
order by 1
;

-- 가장 많이 사용된 채널 -> 채널별 유저수? , 채널별 세션수?
select b.channel
     , count(1) as session_count
     , count(distinct userid) as user_count
from raw_data.session_timestamp a
         inner join raw_data.user_session_channel b on a.sessionid = b.sessionid
group by b.channel
-- order by 2 desc
-- order by 3 desc
;

-- 가장 많은 세션을 만들어낸 사용자 ID?
select b.userid
     , count(1) as session_count
from raw_data.session_timestamp a
         inner join raw_data.user_session_channel b on a.sessionid = b.sessionid
group by b.userid
order by 2 desc
limit 1
;

-- 월별 유니크한 사용자 수
select left(a.ts,7) as mon
     , count(distinct b.userid) as mau
from raw_data.session_timestamp a
         inner join raw_data.user_session_channel b on a.sessionid = b.sessionid
group by 1
order by 1 desc
;

-- 월별 채널별 유니크한 사용자 수
select left(a.ts,7) as mon
     , b.channel
     , count(distinct b.userid) as mau
from raw_data.session_timestamp a
         inner join raw_data.user_session_channel b on a.sessionid = b.sessionid
group by 1 , 2
order by 1 desc, 2
;

-- CTAS
drop table if exists adhoc.shee_session_summary;
create table adhoc.shee_session_summary as
    select b.*, a.ts from raw_data.session_timestamp a
        join raw_data.user_session_channel b on a.sessionid = b.sessionid
;


-- 채널별 월별 매출액
-- paidUsers :  0원 구매한 고객은 카운트하지 않는다
-- conversionRate : 소수점 둘째자리까지 보여준다
drop table if exists adhoc.shee_monthly_channel_summary;
create table adhoc.shee_monthly_channel_summary as
    select a.channel as channel
     , left(b.ts, 7) as month
     , count(distinct a.userid) as uniqueUsers
     , count(distinct case when c.amount > 0 then a.userid end) as paidUsers
     , round(paidUsers::float * 100 / nullif(uniqueUsers,0), 2) as conversionRate
     , sum(c.amount) as grossRevenue
     , sum(case when c.refunded is false then c.amount end) as netRevenue
from raw_data.user_session_channel a
    join raw_data.session_timestamp b on a.sessionid = b.sessionid
    left outer join raw_data.session_transaction c on a.sessionid = c.sessionid
group by 1 , 2
;
