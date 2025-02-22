# LessWrong AI Alignment Trends
End-to-end data engineering project where we extract LessWrong posts information,  

# Data Diagram/Workflow
TODO

# ETL Process

## Extract
1. Scraping latest LessWrong posts
- using requests & Beautiful Soup 


2. Storage
- after scraping the latest n posts, we store the raw data on AWS S3 as object storage