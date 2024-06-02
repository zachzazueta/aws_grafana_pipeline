import sys
import boto3

client = boto3.client('athena')

SOURCE_TABLE_NAME = 'magsev_polygon_kinesis_fp'
NEW_TABLE_NAME = 'polygon_parquet_fp'
NEW_TABLE_S3_BUCKET = 's3://polygon-parquet-fp-bucket-1/'
MY_DATABASE = 'fp_db_polygon_io'
QUERY_RESULTS_S3_BUCKET = 's3://query-results-location-polygon-fp'

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE {NEW_TABLE_NAME} WITH
    (external_location='{NEW_TABLE_S3_BUCKET}',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['ts'])
    AS

    SELECT
        ticker
        ,high
        ,low
        ,high-low AS hourly_var
        ,ts
    FROM "{MY_DATABASE}"."{SOURCE_TABLE_NAME}"

    ;
    """,
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_S3_BUCKET}'}
)

# list of responses
resp = ["FAILED", "SUCCEEDED", "CANCELLED"]

# get the response
response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])

# wait until query finishes
while response["QueryExecution"]["Status"]["State"] not in resp:
    response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])
    
# if it fails, exit and give the Athena error message in the logs
if response["QueryExecution"]["Status"]["State"] == 'FAILED':
    sys.exit(response["QueryExecution"]["Status"]["StateChangeReason"])
