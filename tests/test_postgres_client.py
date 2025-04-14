from postgres_client import PostgresClient
import uuid
from add_types import InputDatabaseData, SelectDatabaseData
import json
import pytest

@pytest.mark.order1
def test_initialization():
    expected_error = False
    error = None
    try:
        client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")
        error = False
    except Exception as e:
        print(e)
        error = True
    assert expected_error == error

@pytest.mark.order2
def test_data_push():
    expected_error = [False, False, False]
    error = []
    client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")
    client.connection.execute("DELETE FROM linkup_monitor WHERE query = 'This doesn''t make sense' AND duration = 1")
    data = [{"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This doesn't make sense", "output_type": "searchResults", "search_type": "standard", "duration": 1}, {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This doesn't make sense", "output_type": "searchResults", "search_type": "standard", "duration": 1}, {"call_id": str(uuid.uuid4()), "status_code": 500, "query": "This doesn't make sense", "output_type": "searchResults", "search_type": "standard", "duration": 1}]
    for d in data:
        dt = InputDatabaseData.model_validate_json(json.dumps(d))
        try:
            client.push_data(dt)
            error.append(False)
        except Exception as e:
            error.append(True)
    assert expected_error == error

@pytest.mark.order3
def test_data_pull():
    test_inputs = [
        None,
        {"created_at": False, "status_code": 200, "output_type": None, "search_type": None, "limit": 10, "query": "This doesn't make sense"},
        {"created_at": None, "status_code": None, "output_type": None, "search_type": "deep", "limit": None,"query": "This doesn't make sense"},
        {"created_at": None, "status_code": None, "output_type": None, "search_type": None, "limit": 2, "query": "This doesn't make sense"},
        {"created_at": True, "status_code": None, "output_type": None, "search_type": None, "limit": None, "query": "This doesn't make sense"},
    ]
    expected_outputs = [True, True, True, True, True]
    outputs = []
    for t in range(len(test_inputs)):
        try:
            client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")
            if test_inputs[t] is not None:
                dt = SelectDatabaseData.model_validate_json(json.dumps(test_inputs[t]))
                output_data = client.pull_data(dt)
                if t == 1 or t == 3:
                    outputs.append(len(output_data)==2)
                elif t == 4:
                    outputs.append(len(output_data)==3)
                else:
                    outputs.append(len(output_data)==0)
            else:
                output_data = client.pull_data(test_inputs[t])
                outputs.append(len(output_data)>=3)
        except Exception as e:
            print(e)
            outputs.append(None)
    assert expected_outputs == outputs