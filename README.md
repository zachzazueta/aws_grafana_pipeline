# AWS -> Grafana - my first cloud hosted data pipeline
For this project, I worked through the process to get data from a raw API call, to become cleaned and structured data in an Athena database, and then queryied into a datamart to sit beneath a dashboard in Grafana.

To dive into the world of data engineering, I recently completed a short course hosted by David Freitag - it was a great course with straightforward instruction, clear materials, and it provided me the skills to develop this basic project and the know-how to continue building upon it. I highly recommend David as an instructor - you can find his class here on Maven: https://maven.com/david-freitag/first-serverless-de-project.

# The Objective
My goal was to gain familiarity with AWS and learn more about data engineering. As a bonus, I got an introduction to Grafana as a new data viz tool.

# The Outcome
As stated above, David delivered quality instruction, and I learned the basics for how to develop a workflow in Glue that would ingest data from an API call with Lambdas and Kinesis Firehose, structure that data in S3, query it with Athena, run quality assurance checks, and write a production table back to an Athena database. We took it a step further and built out a dashboard to visualize this data in Grafana, therefore developing a fully fledged data pipeline.

Here is a diagram of the steps taken in this project:
![image](https://github.com/zachzazueta/aws_grafana_pipeline/assets/64451230/e21ed949-13f7-43e1-ac83-7f149a571498)

I elected to pull stock ticker data from Polygon.io and build a dashboard that presented the hourly varience in price of the "Magnificent 7" - the seven stocks that were accounting for approximately 30% of the S&P 500 as of Q1 2024, namely Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta, and Tesla.

# The Output
Here is the view of a nacient dashboard, fed by my Athena database. As stated, the view shows the absolute hourly varience in price of the stock, allowing the viewer to see spikes and get a sense of volatility.
![image](https://github.com/zachzazueta/aws_grafana_pipeline/assets/64451230/de80608f-605a-4761-8be5-d331fea1f203)

# The Process
## Data sourcing
I decided to use the API from Polygon.io, a site that provides free calls to stock tickers with end of day information, including a stock's high price, low price, open price, close price, etc. A user can pull this data at various time intervals - I selected to get the hourly high and low. 

## Data ingestion
The first step was to build a Lambda function that would dump data into a Kinesis firehose. 
Kinesis Firehoses are a great method to batch data ingestion, as it captures data from the source and writes it to S3. During this step, I wrote a Lambda function (Polygon_to_firehose). This function would call the API using a urllib3 request; the call would return data in json format, which I then parsed and generated a structured dictionary with the columns I wanted; each structured dictionary was added to an output string that was ultimately fed into the firehose put_record function as a structured data table.  The firehose dumped data into s3://polygon-kinesis-fp/.

The free level of Polygon's service does limit the number of calls that can be made in a minute, and since I had to pull the data one ticker at a time, I introduced a lag function to the script used to call the API.

If this pipeline were to become something I used regularly, or was part of a business process, I could use an EventBridge trigger to run this firehose at the top of the Glue workflow.

## Building a pipeline in Glue + ETL
Once the data was in an S3 bucket, I was ready to further manipulate it. I would do this via a Glue Workflow, running a number of ETL jobs.
The first step of the workflow was to run a Crawler. The Crawler (first_pass_polygon_crawler) parsed through the S3 bucket that the firehose was pointed at, s3://polygon-kinesis-fp/. It then returned the parsed data to the Athena database (fp_db_polygon_io) after adding a specified prefix (magsev_) to the table name. I now had a key table in the database (magsev_polygon_kinesis_fp).

The Glue workflow then needed to run a series of ETL jobs. The first of these (delete_parquet_polygon_table_s3_athena) was designed to find an existing table in the database, delete the parquet table (polygon_parquet_fp - which would only exist after the first run of this process). Deleting existing data as a first step is important, because if I were to simply write new data to the existing table, there is a liklihood I would end up with duplicate data.

The second step was creating a parquet table of the main (magsev_polygon_kinesis_fp) table. Storing data in parquet format offers data efficiency for later queries, as it allows for selecting specific columns, instead of querying all rows and then finding records that match. Using the job create_parquet_polygon_table, I ran a SQL Create Table query wrapped in python, formatting it as Parquet and partitioning it by the time column. Partitioning out the time column would allow me to later select certain hours or days of data more easily.

The next step was to run a series of data quality checks on the newly created parquet table. The job (dp_checks_parquet_polygon_table) examined two columns I consider to be critical - namely the hourly_var column which I generated in the previous step to calculate the variance between high and low hourly price, as well as the ticker column. The checks would cause the workflow to break if there were any Null values in the hourly_var column or if there were fewer than 7 distinct tickers in the final output, as that would have indicated the source data pull was incomplete.

The final job was to write the parquet table to a Production folder (s3://parquet-polygon-table-prod-1) as a production version of the table (polygon_parquet_fp_PROD). The production instance will serve as a source of truth for anyone querying the data (analysts, data scientists, BI team...).

Throughout the workflow, there were triggers between each of these steps, that would only allow the next step to run if the previous step succeded. If a step were to fail, I was able to access Error Logs in CLoudwatch to assess the problem.

![image](https://github.com/zachzazueta/aws_grafana_pipeline/assets/64451230/061d7073-3fbb-4ebd-91c1-c8e31a454307)

## Designing a dashboard
As mentioned above, we used Grafana, a web-based dashboard design tool, to create a user-friendly dashboard to get some use from our data.

After creating an account, I was able to connect AWS Athena as a data source. I connected to the database (fp_db_polygon_io) and then pointed to the table (the newly published production table, specific to the latest timestamp of output) and then queried for the timestamp to be on the x-axis and the hourly variance to be on the y-axis. By selecting the data to be a timeseries, the graph split out the various tickers into their own distinct marks. I adjusted the "tooltip" to show the individual values when the user hovered over the chart.

![image](https://github.com/zachzazueta/aws_grafana_pipeline/assets/64451230/b6de06b7-7ca6-4c29-af8b-872758c84f9a)

# Next Steps
The data viz is in an MVP state, and isn't delivering significant value to an end user at present - with some additional work, this is where I would take things:
- First, I will index the daily variance of the data, so as to not have the seemingly outlier performance shown in the above screenshot (exhibited by NVDA). I could also aggregate the indexes to show a trend line and see if there are certain stocks that are consistently higher/lower variance than the aggregate.
- A second step will be to add in some additional comparison points - a sample of potentially more volatile investments like crypto assets and a few of the larger indexes (SPY, NDAQ).
- A third step will be to expand the amount of data included, as one week is not substantial for a bigger picture takeaway. This will involve adjusting the API call and accounting for additional partitions as the workflow writes the new table.
