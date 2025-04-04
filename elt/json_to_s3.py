import json
import boto3
import os
import datetime
import logging

def upload_json(json_filename: str = '/opt/airflow/elt/lesswrong_data.json'):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Load JSON data
    try:
        # Try both the absolute path and the relative path
        if os.path.exists(json_filename):
            file_path = json_filename
        else:
            file_path = os.path.join(os.getcwd(), "lesswrong_data.json")
            
        logger.info(f"Loading JSON file from {file_path}")
        with open(file_path, "r") as f:
            json_object = json.load(f)
            
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise FileNotFoundError(f"Could not find or load the JSON file: {e}")
    
    # Upload to S3
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"lesswrong_data_{timestamp}.json"
        
        logger.info("Creating S3 client using IAM role")
        
        # Using IAM role - boto3 will automatically use the role credentials
        # No need to specify credentials when running in an environment with IAM role
        s3 = boto3.client('s3')
        
        logger.info(f"Uploading to S3 bucket: lw-trends, key: {save_filename}")
        s3.put_object(
            Body=json.dumps(json_object),
            Bucket='lw-trends',
            Key=save_filename
        )
        
        logger.info(f"Successfully uploaded {save_filename} to S3 bucket lw-trends")
        return f"s3://lw-trends/{save_filename}"
        
    except Exception as e:
        logger.error(f"S3 upload error: {e}")
        raise Exception(f"Failed to upload to S3: {str(e)}")

if __name__ == "__main__":
    upload_json()