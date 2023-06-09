-- [3일차 과제] nps.csv를 기반으로 월별 NPS 계산하기

CREATE SCHEMA raw_data;
CREATE SCHEMA analytics;

CREATE TABLE raw_data.nps (
    created_at TIMESTAMP,
    score      SMALLINT
);

-- 4. bulkinsert
COPY raw_data.nps
    FROM 's3://shee-test-bucket/temp_data/nps.csv'
    IAM_ROLE 'arn:aws:iam::884988372765:role/redshift.read.s3'
    DELIMITER ','
    REMOVEQUOTES
    DATEFORMAT 'auto'
    TIMEFORMAT 'auto'
    IGNOREHEADER 1
;

-- 데이터 품질 검토 (갯수, 순서, null)
SELECT COUNT(1)
FROM raw_data.nps;

SELECT *
FROM raw_data.nps
ORDER BY created_at DESC
LIMIT 1;

SELECT COUNT(CASE WHEN nps.created_at IS NULL THEN 1 END) created_at_count
     , COUNT(CASE WHEN nps.score IS NULL THEN 1 END)      score_count
FROM raw_data.nps;


-- 5. nps_summary 테이블 생성
CREATE TABLE analytics.nps_summary AS
SELECT LEFT(created_at, 7)                                AS month
     , ROUND(SUM(CASE
                     WHEN score >= 9 AND score <= 10 THEN 1
                     WHEN score >= 0 AND score <= 6 THEN -1 END
                 )::FLOAT * 100 / NULLIF(COUNT(1), 0), 2) AS nps
FROM raw_data.nps a
GROUP BY 1
ORDER BY 1;

SELECT *
FROM analytics.nps_summary;