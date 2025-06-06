# LessWrong AI Alignment Trends
End-to-end data engineering project where we extract LessWrong posts information, and visualize trends in AI Alignment posts.

## ETL Process
The pipeline is orchestrated by Airflow DAGs.

### Extract
1. Scraping latest LessWrong posts using requests & Beautiful Soup to get the raw html information
Here I'm using Selenium for scraping dynamic content from LessWrong.
2. Extract information from the HTML like title, author name, post tags and karma.  

### Load
After scraping the posts, we store the raw JSON file with the data on AWS S3 as object storage in a general purpose bucket. 
I upload the data using the AWS SDK boto3.

### Transform
Initially the modeling will be simple: we'll only use the existing tags from the posts.
We do some processing on the tags using a dbt layer:
- eliminate the posts with the "meta" tag (those are meta posts on LessWrong we're not interested in).

## Modeling
Topic Modeling using BERTopic
- naive approach using pretrained sentence transformers 
    - further finetune the topics found
- semi-supervised topic modeling - using the existing tags to inform the clusters 
- dynamic topic modeling to model changes in topics over time 



## TODOs:
1. visualizations:
    - topic clusters with size of points based on karma
2. modelling
    - topic modelling using e.gg k-means clustering, LDA 
3. testing
4. deployment


3. bugfixes 
    - 
4. features:
    - data modeling (OLAP, star/snowflake schema)
    - LLM for topic modelling
    - add secrets management
    - Add Apache Kafka for streaming data
    - data diagram/Workflow

