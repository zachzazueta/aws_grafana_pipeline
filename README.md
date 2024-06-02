# AWS -> Grafana - my first serverless data pipeline
Working process to get data from a raw API call to a dashboard in Grafana


To dive into the world of data engineering, I recently completed a short course hosted by David Freitag - it was a great course with straightforward instruction, clear materials, and it provided me the skills to develop this basic project and the know-how to continue building upon it. I highly recommend David as an instructor - you can find his class here on Maven: https://maven.com/david-freitag/first-serverless-de-project.

# The Object
My goal was to gain familiarity with AWS and learn more about data engineering.

# The Outcome
David delivered, and I learned the basics for how to develop a workflow in Glue that would ingest data from an API call with Lambdas and Kinesis Firehose, structure that data in S3, query it with Athena, run quality assurance checks, and write a production table back to an Athena database. We took it a step further and built out a dashboard to visualize this data in Grafana, therefore developing a fully fledged data pipeline.

I elected to pull stock ticker data from Polygon.io and build a dashboard that presented the hourly varience in price of the "Magnificent 7" - the seven stocks that were accounting for approximately 30% of the S&P 500 as of Q1 2024, namely Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta, and Tesla.

# The Output
![image](https://github.com/zachzazueta/aws_grafana_pipeline/assets/64451230/de80608f-605a-4761-8be5-d331fea1f203)

# The Process
## Data sourcing
I decided to use the API from Polygon IO
## Data ingestion
The first step was to build a Lambda function that would dump data into a Kinesis firehose. The firehose dumped data into s3://polygon-kinesis-fp/
Reasons to use a firehose...
## Building a pipeline in Glue + ETL
The first step of the pipeline was to run a Crawler. The Crawler (first_pass_polygon_crawler) parsed through the S3 bucket that the firehose was pointed at, s3://polygon-kinesis-fp/. It then returned the parsed data to the Athena database (fp_db_polygon_io) after adding a specified prefix (magsev_) to the table name. I now had a key table in the database.

The Glue workflow then needed to run a series of jobs. The first of these (delete_parquet_polygon_table_s3_athena) was designed to find an existing table in the database, delete the parquet table (polygon_parquet_fp) 
## Designing a dashboard

# Next Steps
- My immediate next step will be to index the daily variance of the data, so as to not have the seemingly outlier performance shown in the above screenshot (exhibited by NVDA)
- A second step will be to add in some additional comparison points - a sample of potentially more volatile investments like crypto assets and a few of the larger indexes (SPY, NDAQ)
