-- 1. listagg
select userid, listagg(channel, ',') within group ( order by userid)
from raw_data.user_session_channel usc
group by 1
limit 10
;


-- 2. LAG
SELECT usc.*, st.ts, LAG(channel, 1) OVER (PARTITION BY userId ORDER BY ts DESC) prev_channel
FROM raw_data.user_session_channel usc
         JOIN raw_data.session_timestamp st ON usc.sessionid = st.sessionid
ORDER BY usc.userid, st.ts
LIMIT 100;

-- 3. JSON
SELECT JSON_EXTRACT_PATH_TEXT('{
  "f2": {
    "f3": "1"
  },
  "f4": {
    "f5": "99",
    "f6": "star"
  }
}', 'f4', 'f6');


SELECT JSON_EXTRACT_PATH_TEXT('{
  "f2": {
    "f3": "1"
  },
  "f4": {
    "f5": "99",
    "f6": "star"
  }
}', 'f4');