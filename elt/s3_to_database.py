import boto3

def get_latest_s3_key(bucket):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)

    files = [obj['Key'] for obj in response.get('Contents', [])]
    latest_file = sorted(files)[-1]  # assuming filenames have timestamps
    return latest_file

if __name__ == "__main__":
    get_latest_s3_key(bucket="lw-trends")