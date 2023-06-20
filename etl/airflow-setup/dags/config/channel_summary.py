{
    'table': 'channel_summary',
    'schema': 'gracia10',
    'main_sql': """
            SELECT a.channel AS channel
                 , LEFT(b.ts, 7) AS month
                 , COUNT(DISTINCT a.userid) AS uniqueusers
                 , COUNT(DISTINCT CASE WHEN c.amount > 0 THEN a.userid END) AS paidusers
                 , ROUND(paidusers::FLOAT * 100 / NULLIF(uniqueusers,0), 2) AS conversionrate
                 , SUM(c.amount) AS grossrevenue
                 , SUM(CASE WHEN c.refunded IS FALSE THEN c.amount END) AS netrevenue
              FROM raw_data.user_session_channel a
              JOIN raw_data.session_timestamp b ON a.sessionid = b.sessionid
   LEFT OUTER JOIN raw_data.session_transaction c ON a.sessionid = c.sessionid
          GROUP BY 1 , 2;""",
    'input_check': [],
    'output_check':
        [
            {
                'sql': 'SELECT COUNT(1) FROM gracia10.temp_{table}',
                'count': 42
            }
        ],
}
