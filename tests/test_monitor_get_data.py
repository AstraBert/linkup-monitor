from monitor import LinkupClient, PostgresClient, MonitoredLinkupClient, InputDatabaseData, json, uuid, SelectDatabaseData, pd
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

linkup_client = LinkupClient(api_key=os.environ["LINKUP_API_KEY"])
postgres_client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")
monitored_client = MonitoredLinkupClient(linkup_client, postgres_client)

def fl_in_dir(dirct, ext):
    ls = os.listdir(dirct)
    json_files = [f for f in ls if os.path.isfile(f) and f.endswith(ext)]
    if len(json_files) == 1:
        os.remove(json_files[0])
        return True
    return False

def test_data_raw():
    postgres_client.connection.execute("DELETE FROM linkup_monitor WHERE query = 'This makes sense' AND duration = 3")
    data = [{"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 500, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}]
    for d in data:
        dt = InputDatabaseData.model_validate_json(json.dumps(d))
        postgres_client.push_data(dt)
    output_data = monitored_client.get_data(data=SelectDatabaseData(created_at=None, status_code=None, output_type=None, query = "This makes sense", search_type=None, limit=None), return_mode="raw")
    assert len(output_data) == 3
    assert isinstance(output_data[0], BaseModel) == True

def test_data_json():
    postgres_client.connection.execute("DELETE FROM linkup_monitor WHERE query = 'This makes sense' AND duration = 3")
    data = [{"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 500, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}]
    for d in data:
        dt = InputDatabaseData.model_validate_json(json.dumps(d))
        postgres_client.push_data(dt)
    output_data = monitored_client.get_data(data=SelectDatabaseData(created_at=None, status_code=None, output_type=None, query = "This makes sense", search_type=None, limit=None), return_mode="json", save_to_file=True)
    assert fl_in_dir("./", ".json") == True
    assert len(output_data) == 3
    assert isinstance(output_data[0], dict) == True

def test_data_pd():
    postgres_client.connection.execute("DELETE FROM linkup_monitor WHERE query = 'This makes sense' AND duration = 3")
    data = [{"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 200, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}, {"call_id": str(uuid.uuid4()), "status_code": 500, "query": "This makes sense", "output_type": "searchResults", "search_type": "standard", "duration": 3}]
    for d in data:
        dt = InputDatabaseData.model_validate_json(json.dumps(d))
        postgres_client.push_data(dt)
    output_data = monitored_client.get_data(data=SelectDatabaseData(created_at=None, status_code=None, output_type=None, query = "This makes sense", search_type=None, limit=None), return_mode="pandas", save_to_file=True)
    assert fl_in_dir("./", ".csv") == True
    assert output_data.shape[0] == 3
    assert isinstance(output_data, pd.DataFrame) == True