from monitor import LinkupClient, SearchInput, PostgresClient, monitor, monitored_search, SelectDatabaseData
import json
from linkup import LinkupSearchResults
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

linkup_client = LinkupClient(api_key=os.environ["LINKUP_API_KEY"])
postgres_client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")

@monitor(pg_client = postgres_client)
def search(linkup_client: LinkupClient, data: SearchInput):
    return monitored_search(linkup_client, data)

def test_monitor_search():
    postgres_client.connection._execute_query("DELETE FROM linkup_monitor WHERE query = 'Who won the Nobel prize in 2021?' AND output_type = 'searchResults' AND search_type = 'standard';")
    postgres_client.connection._execute_query("DELETE FROM linkup_monitor WHERE query = 'What were Microsoft revenue and operating income in USD in the fiscal year 2022?' AND output_type = 'structured' AND search_type = 'standard';")
    test_inputs = [
        {
            "query": "Who won the Nobel prize in 2021?",
            "output_type": "searchResults",
            "output_schema": None, 
            "depth": "standard",
        },
        {
            "query": "What were Microsoft revenue and operating income in USD in the fiscal year 2022?",
            "output_type": "structured",
            "output_schema": "{\"properties\": {\"company\": {\"description\": \"Company name\",\"type\": \"string\"},\"fiscalYear\": {\"description\": \"The fiscal year for the reported data\",\"type\": \"string\"},\"operatingIncome\": {\"description\": \"Microsoft's operating income in USD\",\"type\": \"number\"},\"revenue\": {\"description\": \"Microsoft's revenue in USD\",\"type\": \"number\"}},\"type\": \"object\"}", 
            "depth": None,
        },
    ]
    expected_outcomes = [(True, True), (True, True)]
    outcomes = []
    for t in test_inputs:
        dt = SearchInput.model_validate_json(json.dumps(t))
        try:
            response = search(linkup_client, dt)
        except Exception as e:
            outcome = (None, None)
            outcomes.append(outcome)
        else:
            try:
                outputdata = postgres_client.pull_data(data = SelectDatabaseData(created_at=None, status_code=None, output_type=None, query=dt.query, search_type=None, limit=None))
            except Exception as e:
                if dt.output_type != "structured":
                    outcome = (isinstance(response, LinkupSearchResults), None)
                    outcomes.append(outcome)
                else:
                    truth = isinstance(response, BaseModel) or isinstance(response, dict) or isinstance(response, dict)
                    outcome = (truth, None)
                    outcomes.append(outcome)
            else:
                if dt.output_type != "structured":
                    outcome = (isinstance(response, LinkupSearchResults), True)
                    outcomes.append(outcome)
                else:
                    truth = isinstance(response, BaseModel) or isinstance(response, dict) or isinstance(response, dict)
                    outcome = (truth, True)
                    outcomes.append(outcome)
    assert expected_outcomes == outcomes


