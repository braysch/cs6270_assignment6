import argparse
import json
import time
import logging

from django.utils.datetime_safe import datetime

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

logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s %(levelname)s %(message)s",
      filename="consumer.log"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("Running main function...")
    n = 1
    while True:
        key, request = fetch_request(request_bucket)
        if request is not None:
            try:
                data = json.loads(request) # convert json string to python dictionary
                request_type = data.get("type")
                widget_id = data.get("widgetId")
                print ("\nProcessing request of type " + request_type + " with widget_id: " + widget_id + " [" + str(n) + "]")
                logger.info("Processing request of type " + request_type + " with widget_id: " + widget_id + " [" + str(n) + "]")
                n = n+1
                match request_type:
                    case "create":
                        print("Storing data to " + widget_destination + " (" + storage_target + ")")
                        logger.info("Storing data to " + widget_destination + " (" + storage_target + ")")
                        success = store_widget(storage_target, data, widget_destination)
                        if success:
                            print("Item stored successfully")
                            logger.info("Item stored successfully")
                        else:
                            print("Failed to store item")
                            logger.info("Failed to store item")
                    case "update":
                        print("This type is not yet implemented - skipping")
                        logger.info("This type is not yet implemented - skipping")
                    case "delete":
                        print("This type is not yet implemented - skipping")
                        logger.info("This type is not yet implemented - skipping")
                    case _:
                        print("Unknown request type: " + request_type)
                        logger.info("Unknown request type: " + request_type)
            except Exception as e:
                print("Error processing request: " + str(e))
                logger.info("Error processing request: " + str(e))
            if key is not None:
                delete_request(request_bucket, key)
        else:
            time.sleep(0.1)
