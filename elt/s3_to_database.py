import boto3
import subprocess
import psycopg2
import os
import json

def get_latest_key(bucket) -> str:
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)

    files = [obj['Key'] for obj in response.get('Contents', [])]
    latest_file = sorted(files)[-1]  # assuming filenames have timestamps

    return latest_file

def download_s3_file(bucket, key, local_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, local_path)
    return local_path
    

def json_to_database(bucket, filename):

    # Database connection details
    db_config = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'pwd',
        'host': 'destination_postgres',
        'port': '5432'
    }
    
    # Download the file from S3
    local_filename = os.path.basename(filename)
    download_s3_file(bucket, filename, local_filename)
    
    # Determine table name from filename (without extension)
    table_name = local_filename
    if '.' in table_name:
        table_name = table_name.split('.')[0]
    
    # Clean table name for SQL (remove special characters)
    table_name = ''.join(char for char in table_name if char.isalnum() or char == '_')
    
    # Load the JSON data
    with open(local_filename, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file might not be JSON
            print(f"Error: {local_filename} is not valid JSON")
            return

    print(isinstance(data, list), data)

    # Approach 1: For structured JSON that should become a table
    if isinstance(data, dict) and len(data) > 0:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Create table based on the first object's structure
        columns = list(data["posts"][0].keys())
        column_defs = [f'"{col}" TEXT' for col in columns]

        print("columns: ", column_defs)
        
        # Create table
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id SERIAL PRIMARY KEY,
            {', '.join(column_defs)}
        )
        """
        cur.execute(create_table_sql)
        
        # Insert data
        for row in data["posts"]:
            print("ROW:", row)
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join([f'"{col}"' for col in columns])
            values = [row.get(col, None) for col in columns]
            
            insert_sql = f"""
            INSERT INTO "{table_name}" ({columns_str})
            VALUES ({placeholders})
            """
            cur.execute(insert_sql, values)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Data loaded into table '{table_name}' successfully")

    # source_config = {
    # 'dbname': 'destination_db',
    # 'user': 'postgres',
    # 'password': 'pwd',
    # 'host': 'destination_postgres'
    # }
    # destination_filename = filename.split(sep=".")[0]

    # # expose the password for PG
    # subprocess_env = dict(PGPASSWORD=source_config['password'])

    # result = subprocess.run(['pg_dump',
    #                         '-h', source_config['host'],
    #                         '-U', source_config['user'],
    #                         '-d', source_config['dbname'],
    #                         '-f', f'{destination_filename}.sql',
    #                         '-w'], env=subprocess_env, check=True)

if __name__ == "__main__":
    filename = get_latest_key(bucket="lw-trends")
    json_to_database(bucket="lw-trends", filename=filename)