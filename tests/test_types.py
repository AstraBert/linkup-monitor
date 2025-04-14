from add_types import InputDatabaseData, SearchInput, SelectDatabaseData, OutputDatabaseData, json
from pydantic import ValidationError
import uuid

def test_input_db_data():
    test_inputs = [
        {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "Test", "output_type": "searchResults", "search_type": "standard", "duration": 1},
        {"call_id": str(uuid.uuid4()), "status_code": 200, "query": 3, "output_type": "searchResults", "search_type": "standard", "duration": 1},
        {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "Test", "output_type": "searchResult", "search_type": "standard", "duration": 1},
        {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "Test", "output_type": "searchResults", "search_type": "standar", "duration": 1}
    ]
    expected_outputs = [1,0,0,0]
    outputs = []
    for t in test_inputs:
        try:
            o = InputDatabaseData.model_validate_json(json.dumps(t))
            outputs.append(1)
        except ValidationError:
            outputs.append(0)
    assert expected_outputs == outputs

def test_select_db_data():
    test_inputs = [
        {"created_at": False, "status_code": None, "output_type": "searchResults", "search_type": None, "limit": 1, "query": None},
        {"created_at": None, "status_code": None, "output_type": None, "search_type": None, "limit": None, "query": None},
        {"created_at": False, "status_code": 200, "output_type": "searchResult", "search_type": None, "limit": None, "query": None},
        {"created_at": False, "status_code": None, "output_type": "searchResults", "search_type": "standar", "limit": 1, "query": None},
    ]
    expected_outputs = [1,1,0,0]
    outputs = []
    for t in test_inputs:
        try:
            o = SelectDatabaseData.model_validate_json(json.dumps(t))
            outputs.append(1)
        except ValidationError:
            outputs.append(0)
    assert expected_outputs == outputs

def test_output_db_data():
    test_inputs = [
        {
            "identifier": 0,
            "timestamp": "a timestamp",
            "call_id": str(uuid.uuid4()),
            "status_code": 200,
            "query": "I tried this",
            "output_type": "searchResults",
            "search_type": "standard",
            "duration": 2.03,
        },
        {
            "identifier": 0,
            "timestamp": "a timestamp",
            "call_id": str(uuid.uuid4()),
            "status_code": 200,
            "query": 3,
            "output_type": "searchResults",
            "search_type": "standard",
            "duration": 2.03,
        },
    ]
    expected_outputs = [1,0]
    outputs = []
    for t in test_inputs:
        try:
            o = OutputDatabaseData.model_validate_json(json.dumps(t))
            outputs.append(1)
        except ValidationError:
            outputs.append(0)
    assert expected_outputs == outputs


def test_search_data():
    test_inputs = [
        {
            "query": "test",
            "output_type": "searchResults",
            "output_schema": None, 
            "depth": "deep",
        },
        {
            "query": "test",
            "output_type": "structured",
            "output_schema": None, 
            "depth": "deep",
        },
        {
            "query": "test",
            "output_type": "structured",
            "output_schema": "a", 
            "depth": "deep",
        },
        {
            "query": "test",
            "output_type": "structured",
            "output_schema": "{\"properties\": {\"company\": {\"description\": \"Company name\",\"type\": \"string\"},\"fiscalYear\": {\"description\": \"The fiscal year for the reported data\",\"type\": \"string\"},\"operatingIncome\": {\"description\": \"Microsoft's operating income in USD\",\"type\": \"number\"},\"revenue\": {\"description\": \"Microsoft's revenue in USD\",\"type\": \"number\"}},\"type\": \"object\"}", 
            "depth": "deep",
        },
        {
            "query": "test",
            "output_type": "searchResult",
            "output_schema": None, 
            "depth": "deep",
        },
        {
            "query": "test",
            "output_type": "searchResults",
            "output_schema": None, 
            "depth": "dee",
        },
    ]
    expected_outputs = [1,0,0,1,0,0]
    outputs = []
    for t in test_inputs:
        try:
            o = SearchInput.model_validate_json(json.dumps(t))
            outputs.append(1)
        except ValidationError:
            outputs.append(0)
    assert expected_outputs == outputs