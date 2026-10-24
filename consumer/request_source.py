import boto3

client = boto3.client("s3")

def fetch_request(bucket): # fetch the next request
    response = client.list_objects_v2(
        Bucket=bucket,
        MaxKeys = 1
    )
    # print(response)
    if "Contents" not in response:
        return None, None
    key = response["Contents"][0]["Key"]
    obj = client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")

    print("key="+key)
    print("body="+body)

    return key, body

def delete_request(bucket, key): # delete request after reading
    client.delete_object(Bucket=bucket, Key=key)