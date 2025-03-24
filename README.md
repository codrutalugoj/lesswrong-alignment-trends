# LessWrong AI Alignment Trends
End-to-end data engineering project where we extract LessWrong posts information, and visualize trends in AI Alignment posts.

## ETL Process

### Extract
1. Scraping latest LessWrong posts using requests & Beautiful Soup to get the raw html information
2. Extract information from the HTML like title, author name, post tags and karma.  

### Transform
Databricks notebooks 

### Load
After scraping the posts, we store the raw JSON file with the data on AWS S3 as object storage in a general purpose bucket. 
TODO: We load the transformed data into a data warehouse/lake



## TODOs:
1. visualizations:
    - topic clusters with size of points based on karma
2. create ELT DAG for automated ELT pipeline using Airflow
    - check DAG in webserver
- add IAM profile or secrets management
- Add Apache Kafka for streaming data
- Data Diagram/Workflow
3. bugfixes 
    - the main page I'm scraping from only contains 16 posts. Should get the data from a different page/using a different method.
4. features:
    - data modeling (OLAP, star/snowflake schema)

