WITH src_user_variant AS (
    SELECT *
    FROM raw_data.user_variant
                         )
SELECT user_id, variant_id
FROM
    src_user_variant