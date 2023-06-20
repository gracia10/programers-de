{
    'table': 'nps_summary',
    'schema': 'gracia10',
    'main_sql': """
                SELECT LEFT(created_at, 10) AS date,
                  ROUND(SUM(CASE
                    WHEN score >= 9 THEN 1 
                    WHEN score <= 6 THEN -1 END)::FLOAT*100/COUNT(1), 2)
                FROM gracia10.nps
                GROUP BY 1
                ORDER BY 1;""",
    'input_check':
        [
            {
                'sql': 'SELECT COUNT(1) FROM gracia10.nps',
                'count': 150000
            },
        ],
    'output_check':
        [
            {
                'sql': 'SELECT COUNT(1) FROM {schema}.temp_{table}',
                'count': 12
            }
        ],
}
