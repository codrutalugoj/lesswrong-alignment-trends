import json
import boto3   
import os 
import datetime

def upload_json(json_filename: str = '/opt/airflow/elt/lesswrong_data.json'):
    try:
        # Check if file exists
        if not os.path.exists(json_filename):
            raise FileNotFoundError(f"JSON file not found: {json_filename}")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"lesswrong_data_{timestamp}.json"

        with open(json_filename, "r") as f:
            json_object = json.load(f)

        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(json_object),
            Bucket='lw-trends',
            Key=save_filename
        )
    except Exception as e:
        print(f"Error uploading JSON to S3: {e}")

if __name__ == "__main__":
    upload_json()