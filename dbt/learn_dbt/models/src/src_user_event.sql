WITH src_user_event AS (
    SELECT *
    FROM raw_data.user_event
                       )
SELECT user_id, datestamp, item_id, clicked, purchased, paidamount
FROM
    src_user_event