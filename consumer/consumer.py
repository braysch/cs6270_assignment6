import argparse
import json
import time

from widget_storage import store_widget
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
    while True:
        key, request = fetch_request(request_bucket)
        if request is not None:
            try:
                data = json.loads(request) # convert json string to python dictionary
                request_type = data.get("type")
                widget_id = data.get("widgetId")
                print ("request_type="+request_type+", widget_id="+widget_id)
                match request_type:
                    case "create":
                        store_widget(storage_target, data, widget_destination)
                    case "update":
                        pass
                    case "delete":
                        pass
                    case _: print("Unknown request type: " + request_type)
            except Exception as e:
                print("Error processing request: " + str(e))
            if key is not None:
                delete_request(request_bucket, key)
        else:
            time.sleep(0.1)
