import boto3

client = boto3.client("s3")

def fetch_request(bucket): # fetch the next request
    response = client.list_objects_v2(
        Bucket=bucket,
        MaxKeys = 1
    )
    print(response)

def delete_request(bucket, key): # delete request after reading
    client.delete_object(Bucket=bucket, Key=key)