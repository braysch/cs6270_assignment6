import argparse

from request_source import fetch_request, delete_request

parser = argparse.ArgumentParser(description="My program")
parser.add_argument("--request-bucket", required=True, help="s3 bucket where producer writes to and the consumer reads from")
parser.add_argument("--storage-target", required=True, choices=["s3", "dynamodb"], help="Either 's3' or 'dynamodb'")
parser.add_argument("--widget-destination", required=True, help="s3 bucket or dynamodb table where consumer writes to")
args = parser.parse_args()

# print(args)

request_bucket = args.request_bucket
storage_target = args.storage_target
widget_destination = args.widget_destination

if __name__ == "__main__":
    print("Running main function...")
    key, request = fetch_request(request_bucket)
    delete_request(request_bucket, key)
