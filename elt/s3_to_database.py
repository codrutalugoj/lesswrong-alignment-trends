import boto3
import subprocess

def get_latest_s3_key(bucket) -> str:
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)

    files = [obj['Key'] for obj in response.get('Contents', [])]
    latest_file = sorted(files)[-1]  # assuming filenames have timestamps
    return latest_file

def json_to_database(filename: str):
    source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'pwd',
    'host': 'postgres'
    }
    destination_filename = filename.split(sep=".")[0]

    result = subprocess.run(['pg_dump',
                            '-h', source_config['host'],
                            '-U', source_config['user'],
                            '-d', source_config['dbname'],
                            '-f', f'{destination_filename}.sql',
                            '-w'], check=True)

if __name__ == "__main__":
    filename = get_latest_s3_key(bucket="lw-trends")
    json_to_database(filename=filename)