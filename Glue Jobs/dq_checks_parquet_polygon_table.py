import sys
import awswrangler as wr

# this check counts the number of NULL rows in the hourly_variance column
# if any rows are NULL, the check returns a number > 0
NULL_DQ_CHECK = f"""
SELECT 
    SUM(CASE WHEN hourly_var IS NULL THEN 1 ELSE 0 END) AS res_col
FROM "fp_db_polygon_io"."polygon_parquet_fp"
;
"""

# run the quality check
df = wr.athena.read_sql_query(sql=NULL_DQ_CHECK, database="fp_db_polygon_io")

# exit if we get a result > 0
# else, the check was successful
if df['res_col'][0] > 0:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')
    
# this check counts the number of unique tickers the ticker column
# if there are fewer than expected, the check returns a number > 0
ticker_count_check = f"""
SELECT 
    COUNT(DISTINCT ticker) AS res_col
FROM "fp_db_polygon_io"."polygon_parquet_fp"
;
"""

# run the quality check
df = wr.athena.read_sql_query(sql=ticker_count_check, database="fp_db_polygon_io")

# exit if we get a result != 7
# else, the check was successful
if df['res_col'][0] != 7:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')