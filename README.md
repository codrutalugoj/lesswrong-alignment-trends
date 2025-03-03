# LessWrong AI Alignment Trends
End-to-end data engineering project where we extract LessWrong posts information, and visualize trends in AI Alignment posts.

# ETL Process

## Extract
1. Scraping latest LessWrong posts using requests & Beautiful Soup to get the raw html information
2. Extract information from the HTML like title, author name, post tags and karma.  


2. Load
After scraping the posts, we store the raw JSON file with the data on AWS S3 as object storage in a general purpose bucket. 
In the ETL notebook 


# TODOs:
- Data Diagram/Workflow
- visualizations:
    - topic clusters with size of points based on karma
- create ELT DAG for automated ELT pipeline using Airflow
- add IAM profile or secrets management
- Add Apache Kafka for streaming data

