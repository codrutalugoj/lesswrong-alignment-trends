import json
import boto3    

def upload_json(json_filename: str):

    s3 = boto3.client('s3')
    json_object = json.load(json_filename)

    s3.put_object(
        Body=json.dumps(json_object),
        Bucket='lw-trends',
        Key=json_filename
    )
