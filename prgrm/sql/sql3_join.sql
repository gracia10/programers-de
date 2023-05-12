
select * from raw_data.user_session_channel order by userid;
select * from raw_data.session_timestamp;
select * from raw_data.session_transaction;
select * from raw_data.nps;


-- 1. 사용자 별로 처음 채널과 마지막 채널 알아내기
with sub as (
    SELECT a.userid
         , a.channel
         , row_number() OVER (PARTITION BY a.userid ORDER BY b.ts) AS min_rownum
         , row_number() OVER (PARTITION BY a.userid ORDER BY b.ts desc) AS max_rownum
    FROM raw_data.user_session_channel a
             JOIN raw_data.session_timestamp b ON a.sessionid = b.sessionid
)
SELECT userid
     , MAX(CASE WHEN min_rownum = 1 THEN channel END) first_channel
     , MAX(CASE WHEN max_rownum = 1 THEN channel END)  last_channel
FROM sub
group by userid
;




-- 2. Gross Revenue가 가장 큰 userid 10개 찾기
select a.userid
     , sum(b.amount) revenue
from raw_data.user_session_channel a
    join raw_data.session_transaction b on a.sessionid = b.sessionid
group by 1
order by 2 desc
limit 10
;


-- 3. raw_data.nps 테이블을 바랑으로 월별 nps 계산
select left(created_at, 7)
     , sum(case when score >= 0 and score <= 6 then 1 end) * 100.0 / count(1) as detractor
     , sum(case when score >= 7 and score <= 8 then 1 end) * 100.0 / count(1) as passive
     , sum(case when score >= 9 and score <= 10 then 1 end) * 100.0 / count(1) as promoter
     , round(promoter - detractor) as nps
from raw_data.nps a
group by 1
;

