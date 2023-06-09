-- 실습1 환경셋팅

CREATE SCHEMA raw_data;
CREATE SCHEMA analytics;
CREATE SCHEMA adhoc;
CREATE SCHEMA pii;


select * from pg_namespace;


CREATE USER shee PASSWORD '!Tjdgml10';
select * from pg_user;


CREATE GROUP analytics_users;
CREATE GROUP analytics_authors;
CREATE GROUP pii_users;

ALTER GROUP analytics_users ADD USER shee;
ALTER GROUP analytics_authors ADD USER shee;
ALTER GROUP pii_users ADD USER shee;

SELECT * FROM pg_group;


CREATE ROLE staff;
CREATE ROLE manager;
GRANT ROLE staff TO shee;   -- 다른 역할(Role)을 지정 가능
GRANT ROLE staff TO ROLE manager;

select * from SVV_ROLES;


-- 실습2 COPY

CREATE TABLE raw_data.user_session_channel (
    userid integer ,
    sessionid varchar(32) primary key,
    channel varchar(32)
);

COPY raw_data.user_session_channel
    FROM 's3://shee-test-bucket/test_data/user_session_channel.csv'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::884988372765:role/redshift.read.s3'
    DELIMITER ','
    DATEFORMAT 'auto'
    TIMEFORMAT 'auto'
    IGNOREHEADER 1 REMOVEQUOTES;

SELECT * FROM raw_data.user_session_channel LIMIT 10;



CREATE TABLE raw_data.session_timestamp (
    sessionid varchar(32) primary key,
    ts timestamp
);

COPY raw_data.session_timestamp
    FROM 's3://shee-test-bucket/test_data/session_timestamp.csv'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::884988372765:role/redshift.read.s3'
    DELIMITER ','
    DATEFORMAT 'auto'
    TIMEFORMAT 'auto'
    IGNOREHEADER 1 REMOVEQUOTES;

SELECT * FROM raw_data.session_timestamp LIMIT 10;


CREATE TABLE raw_data.session_transaction (
    sessionid varchar(32) primary key,
    refunded boolean,
    amount int
);

COPY raw_data.session_transaction
    FROM 's3://shee-test-bucket/test_data/session_transaction.csv'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::884988372765:role/redshift.read.s3'
    DELIMITER ','
    DATEFORMAT 'auto'
    TIMEFORMAT 'auto'
    IGNOREHEADER 1 REMOVEQUOTES;

SELECT * FROM raw_data.session_transaction LIMIT 10;


-- 실습3 권한
GRANT ALL ON SCHEMA analytics TO GROUP analytics_authors;
GRANT ALL ON ALL TABLES IN SCHEMA analytics TO GROUP analytics_authors;

GRANT ALL ON SCHEMA adhoc to GROUP analytics_authors;
GRANT ALL ON ALL TABLES IN SCHEMA adhoc TO GROUP analytics_authors;

GRANT USAGE ON SCHEMA raw_data TO GROUP analytics_authors;
GRANT SELECT ON ALL TABLES IN SCHEMA raw_data TO GROUP analytics_authors;

GRANT USAGE ON SCHEMA analytics TO GROUP analytics_users;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO GROUP analytics_users;

GRANT ALL ON SCHEMA adhoc to GROUP analytics_users;
GRANT ALL ON ALL TABLES IN SCHEMA adhoc TO GROUP analytics_users;

GRANT USAGE ON SCHEMA raw_data TO GROUP analytics_users;
GRANT SELECT ON ALL TABLES IN SCHEMA raw_data TO GROUP analytics_users;

GRANT USAGE ON SCHEMA pii TO GROUP pii_users;
GRANT SELECT ON ALL TABLES IN SCHEMA pii TO GROUP pii_users;
