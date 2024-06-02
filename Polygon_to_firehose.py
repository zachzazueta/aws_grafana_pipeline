import json
import boto3
import urllib3
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-TjTLt'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()
    
    final_msg = f""
    for i in ['NVDA', 'AAPL', 'META', 'TSLA', 'AMZN', 'GOOGL', 'MSFT']:
        time.sleep(15)
        r = http.request("GET", "https://api.polygon.io/v2/aggs/ticker/{}/range/1/hour/{}/{}?apiKey=d3VmGdlpdlgV7fqQ1QYO0kmj7lzitp7g".format(i, str(dt.datetime.now().date() + relativedelta(days=-7)), str(dt.datetime.now().date())))
    
        # turn it into a dictionary
        r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
        
        for j in range(len(r_dict['results'])):
            # extract pieces of the dictionary
            processed_dict = {}
            processed_dict['ticker'] = r_dict['ticker']
            processed_dict['high'] = r_dict['results'][j]['h']
            processed_dict['low'] = r_dict['results'][j]['l']
            processed_dict['ts'] = str(dt.datetime.fromtimestamp(int(str(r_dict['results'][j]['t'])[:-3])))
            
            msg = f"{processed_dict}" 
            
            final_msg += str(msg) + '\n'

    
    fh = boto3.client('firehose')
    
    reply = fh.put_record(
        DeliveryStreamName=FIREHOSE_NAME,
        Record = {
                'Data': final_msg
                }
    )

    return reply