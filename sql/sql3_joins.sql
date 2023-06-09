select *
from raw_data.user_session_channel
order by userid;
select *
from raw_data.session_timestamp;
select *
from raw_data.session_transaction;
select *
from raw_data.nps;


-- 1. 사용자 별로 처음 채널과 마지막 채널 알아내기

-- 1-1) row_num 함수와 max 꼼수를 응용
with sub as (SELECT a.userid
                  , a.channel
                  , row_number() OVER (PARTITION BY a.userid ORDER BY b.ts)      AS min_rownum
                  , row_number() OVER (PARTITION BY a.userid ORDER BY b.ts desc) AS max_rownum
             FROM raw_data.user_session_channel a
                      JOIN raw_data.session_timestamp b ON a.sessionid = b.sessionid)
SELECT userid
     , MAX(CASE WHEN min_rownum = 1 THEN channel END) first_channel
     , MAX(CASE WHEN max_rownum = 1 THEN channel END) last_channel
FROM sub
group by 1
;

-- 1-2) first , last 함수 응용
SELECT a.userid
     , a.channel
     , first_value(channel)
       OVER (PARTITION BY a.userid ORDER BY b.ts ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)      AS min_rownum
     , last_value(channel)
       OVER (PARTITION BY a.userid ORDER BY b.ts DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS max_rownum
FROM raw_data.user_session_channel a
         JOIN raw_data.session_timestamp b ON a.sessionid = b.sessionid
;

-- 2. Gross Revenue가 가장 큰 userid 10개 찾기

-- 2-1) group by
select a.userid
     , sum(b.amount) revenue
from raw_data.user_session_channel a
         join raw_data.session_transaction b on a.sessionid = b.sessionid
group by 1
order by 2 desc
limit 10
;

-- 2-2) sum over()
select distinct userid
              , sum(b.amount) over (partition by userid) revenue
from raw_data.user_session_channel a
         join raw_data.session_transaction b on a.sessionid = b.sessionid
order by 2 desc
limit 10
;

-- 3. raw_data.nps 테이블을 바랑으로 월별 nps 계산

-- 3-1) count
select left(created_at, 7)                                                 as month
     , count(case when score >= 0 and score <= 6 then 1 end)               as detractor
     , count(case when score >= 7 and score <= 8 then 1 end)               as passive
     , count(case when score >= 9 and score <= 10 then 1 end)              as promoter
     , round((promoter - detractor)::float * 100 / nullif(count(1), 0), 2) as nps
from raw_data.nps a
group by 1
order by 1
;

-- 3-2) sum
select left(created_at, 7)                                as month
     , round(sum(case
                     when score >= 9 and score <= 10 then 1
                     when score >= 0 and score <= 6 then -1 end
                 )::float * 100 / nullif(count(1), 0), 2) as nps
from raw_data.nps a
group by 1
order by 1
;
