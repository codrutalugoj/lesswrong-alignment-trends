# LessWrong AI Alignment Trends
End-to-end data engineering project where we extract LessWrong posts information, and visualize trends in AI Alignment posts.

# Data Diagram/Workflow
TODO

# ETL Process

## Extract
1. Scraping latest LessWrong posts using requests & Beautiful Soup to get the raw html information
2. Extract information from the HTML like title, author name, post tags and karma.  


2. Storage
- after scraping the latest n posts, we store the raw data on AWS S3 as object storage