import json
import boto3

def store_widget(storage_target, data, widget_destination):
    print("Storing data to " + widget_destination + " ("+storage_target+")")
    if storage_target == "s3":
        _store_widget_s3(data, widget_destination)
    else:
        _store_widget_dynamodb(data, widget_destination)

def _store_widget_s3(data, widget_destination):
    key = _build_s3_key(data)
    s3 = boto3.client("s3")
    body = json.dumps(data)
    s3.put_object(Bucket=widget_destination, Key=key, Body=body)

def _store_widget_dynamodb(data, widget_destination):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(widget_destination)
    item = _build_dynamodb_item(data)
    table.put_item(Item=item)

def _build_s3_key(data):
    owner = data["owner"]
    if owner == "" or owner is None:
        owner = "Unknown Owner"
    owner_string = owner.lower().replace(" ", "-")
    widget_id = data["widgetId"]
    key = "widgets/"+owner_string+"/"+widget_id
    return key

def _build_dynamodb_item(data):
    item = {
        "id": data["widgetId"],
        "owner": data["owner"]
    }
    if "label" in data:
        item["label"] = data["label"]
    if "description" in data:
        item["description"] = data["description"]
    if "otherAttributes" in data:
        for attributes in data["otherAttributes"]:
            item[attributes["name"]] = attributes["value"]
        #print(item)
    return item
