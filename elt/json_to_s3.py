import json
import boto3   
import os 
import datetime

def upload_json(json_filename: str = '/opt/airflow/elt/lesswrong_data.json'):
    try:
        json_filename = os.path.join(os.getcwd(), "lesswrong_data.json")
        with open(json_filename, "r") as f:
            json_object = json.load(f)
        
    except Exception as e:
        print(f"Error uploading JSON to S3: {e}")
        raise FileNotFoundError()
        
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"lesswrong_data_{timestamp}.json"        

        print("Before boto3")
        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(json_object),
            Bucket='lw-trends',
            Key=save_filename
        )
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    upload_json()