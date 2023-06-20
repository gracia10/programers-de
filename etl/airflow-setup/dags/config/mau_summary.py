{
    'table': 'mau_summary',
    'schema': 'gracia10',
    'main_sql': """
                SELECT TO_CHAR(a.ts, 'YYYY-MM') AS month,
                       COUNT(DISTINCT b.userid) AS mau
                  FROM raw_data.session_timestamp a
                  JOIN raw_data.user_session_channel b ON a.sessionid = b.sessionid
              GROUP BY 1 """,
    'input_check':
        [
            {
                'sql': 'SELECT COUNT(1) FROM raw_data.user_session_channel a LEFT JOIN raw_data.session_timestamp b ON a.sessionid = b.sessionid',
                'count': 100000
            },
        ],
    'output_check':
        [
            {
                'sql': 'SELECT COUNT(1) FROM {schema}.temp_{table}',
                'count': 7
            }
        ],
}
