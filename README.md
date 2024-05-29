# AWS -> Grafana - my first serverless data pipeline
Working process to get data from a raw API call to a dashboard in Grafana


To dive into the world of data engineering, I recently completed a short course hosted by David Freitag - it was a great course with straightforward instruction, clear materials, and it provided me the skills to develop this basic project and the know-how to continue building upon it. I highly recommend David as an instructor - you can find his class here on Maven: https://maven.com/david-freitag/first-serverless-de-project.

# The Object
My goal was to gain familiarity with AWS and learn more about data engineering.

# The Outcome
David delivered, and I learned the basics for how to develop a workflow in Glue that would ingest data from an API call with Lambdas and Kinesis Firehose, structure that data in S3, query it with Athena, run quality assurance checks, and write a production table back to an Athena database. We took it a step further and built out a dashboard to visualize this data in Grafana, therefore developing a fully fledged data pipeline.

I elected to pull stock ticker data from Polygon.io and build a dashboard that presented the hourly varience in price of the "Magnificent 7" - the seven stocks that were accounting for approximately 30% of the S&P 500 as of Q1 2024, namely Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta, and Tesla.

# The Output

# The Process
## Data sourcing
## Data ingestion
## Building a pipeline in Glue + ETL
## Designing a dashboard

# Next Steps
- My immediate next step will be to index the daily variance of the data, so as to not have the seemingly outlier performance shown in the above screenshot (exhibited by NVDA)
- A second step will be to add in some additional comparison points - a sample of potentially more volatile investments like crypto assets and a few of the larger indexes (SPY, NDAQ)
