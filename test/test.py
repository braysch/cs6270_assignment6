import json
from unittest.mock import patch
import pytest

from consumer.widget_storage import _build_s3_key, _build_dynamodb_item, store_widget


#s3

def test_build_s3_key():
    data = {"owner": "John Schmidt", "widgetId": "abc-123"}
    assert _build_s3_key(data) == "widgets/john-schmidt/abc-123"

def test_build_s3_key_no_spaces():
    data = {"owner": "John", "widgetId": "abc-123"}
    assert _build_s3_key(data) == "widgets/john/abc-123"

def test_build_s3_key_multiple_spaces():
    data = {"owner": "John Jacob Jingle-Heimer Schmidt", "widgetId": "abc-123"}
    assert _build_s3_key(data) == "widgets/john-jacob-jingle-heimer-schmidt/abc-123"

def test_build_s3_key_empty_widget_id():
    data = {"owner": "John Schmidt", "widgetId": ""}
    assert _build_s3_key(data) == "widgets/john-schmidt/"

def test_build_s3_key_missing_widget_id():
    data = {"owner": "John Schmidt"}
    with pytest.raises(KeyError): _build_s3_key(data)

def test_build_s3_key_no_data():
    data = {}
    with pytest.raises(KeyError): _build_s3_key(data)

# dynamodb

def test_build_dynamodb_item():
    data = {
        "type": "WidgetCreateRequest",
        "requestId": "req-001",
        "widgetId": "widget-abc-123",
        "owner": "John Schmidt",
        "label": "Blue Widget",
        "description": "A standard blue widget",
        "otherAttributes": [
            {"name": "color", "value": "blue"},
            {"name": "size", "value": "large"},
            {"name": "weight", "value": "10kg"}
        ]
    }
    item = _build_dynamodb_item(data)
    assert item["id"] == "widget-abc-123"
    assert item["owner"] == "John Schmidt"
    assert item["label"] == "Blue Widget"
    assert item["description"] == "A standard blue widget"
    assert item["color"] == "blue"
    assert item["size"] == "large"
    assert item["weight"] == "10kg"

def test_build_dynamodb_item_no_other_attributes():
    data = {
        "type": "WidgetCreateRequest",
        "requestId": "req-001",
        "widgetId": "widget-abc-123",
        "owner": "John Schmidt",
        "label": "Blue Widget",
        "description": "A standard blue widget",
    }
    item = _build_dynamodb_item(data)
    assert item["id"] == "widget-abc-123"
    assert item["owner"] == "John Schmidt"
    assert item["label"] == "Blue Widget"
    assert item["description"] == "A standard blue widget"
    assert "color" not in item
    assert "size" not in item
    assert "weight" not in item

def test_build_dynamodb_item_other_attributes_empty():
    data = {
        "type": "WidgetCreateRequest",
        "requestId": "req-001",
        "widgetId": "widget-abc-123",
        "owner": "John Schmidt",
        "label": "Blue Widget",
        "description": "A standard blue widget",
        "otherAttributes": []
    }
    item = _build_dynamodb_item(data)
    assert item["id"] == "widget-abc-123"
    assert item["owner"] == "John Schmidt"
    assert item["label"] == "Blue Widget"
    assert item["description"] == "A standard blue widget"
    assert "color" not in item
    assert "size" not in item
    assert "weight" not in item

def test_build_dynamodb_item_empty():
    data = {}
    item = _build_dynamodb_item(data)
    with pytest.raises(KeyError): _build_dynamodb_item(data)

# requests

def test_parse_valid_request():
    request = '{"type": "create", "widgetId": "abc-123", "owner": "John Schmidt"}'
    data = json.loads(request)
    assert data["type"] == "create"
    assert data["widgetId"] == "abc-123"

def test_unknown_request_type():
    request = '{"type": "la;ijdfnoiaevj", "widgetId": "abc-123", "owner": "John Schmidt"}'
    json.loads(request)

# storage

@patch("consumer.widget_storage._store_widget_s3")
def test_store_widget_routes_to_s3(mock_s3):
    data = {"widgetId": "abc-123", "owner": "Alice"}
    store_widget("s3", data, "my-bucket")
    mock_s3.assert_called_once_with(data, "my-bucket")

@patch("consumer.widget_storage._store_widget_dynamodb")
def test_store_widget_routes_to_dynamodb(mock_dynamo):
    data = {"widgetId": "abc-123", "owner": "Alice"}
    store_widget("dynamodb", data, "my-table")
    mock_dynamo.assert_called_once_with(data, "my-table")