import json
import boto3

def store_widget(storage_target, data, widget_destination):
    print("Storing data to " + widget_destination + " ("+storage_target+")")
    if storage_target == "s3":
        _store_widget_s3(data, widget_destination)
    else:
        _store_widget_dynamodb(data, widget_destination)

def _store_widget_s3(data, widget_destination):
    owner = data["owner"].lower().replace(" ", "-")
    widget_id = data["widgetId"]
    key = "widgets/"+owner+"/"+widget_id
    s3 = boto3.client("s3")
    body = json.dumps(data)
    s3.put_object(Bucket=widget_destination, Key=key, Body=body)

def _store_widget_dynamodb(data, widget_destination):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(widget_destination)
    item = {
        "id": data["widgetId"],
        "owner": data["owner"],
        "label": data["label"],
        "description": data["description"]
    }
    for attributes in data["otherAttributes"]:
        item[attributes["name"]] = attributes["value"]
    #print(item)
    table.put_item(Item=item)
