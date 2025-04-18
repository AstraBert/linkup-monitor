from monitor import LinkupClient, PostgresClient, MonitoredLinkupClient, SearchInput, json, SelectDatabaseData
from pydantic import BaseModel
from linkup import LinkupSourcedAnswer, LinkupSearchResults
from dotenv import load_dotenv
import os

load_dotenv()

linkup_client = LinkupClient(api_key=os.environ["LINKUP_API_KEY"])
postgres_client = PostgresClient(host="localhost", port=5432, user="localhost", password="admin", database="postgres")
monitored_client = MonitoredLinkupClient(linkup_client, postgres_client)

def test_search():
    postgres_client.connection._execute_query("DELETE FROM linkup_monitor WHERE query = 'Who won the Nobel prize in 2021?' AND output_type = 'searchResults' AND search_type = 'standard';")
    postgres_client.connection._execute_query("DELETE FROM linkup_monitor WHERE query = 'What is the difference between a compiled and an interpreted programming language?' AND output_type = 'sourcedAnswer' AND search_type = 'deep';")
    postgres_client.connection._execute_query("DELETE FROM linkup_monitor WHERE query = 'What were Microsoft revenue and operating income in USD in the fiscal year 2022?' AND output_type = 'structured' AND search_type = 'standard';")
    test_inputs = [
        {
            "query": "Who won the Nobel prize in 2021?",
            "output_type": "searchResults",
            "output_schema": None, 
            "depth": "standard",
        },
        {
            "query": "What is the difference between a compiled and an interpreted programming language?",
            "output_type": "sourcedAnswer",
            "output_schema": None, 
            "depth": "deep",
        },
        {
            "query": "What were Microsoft revenue and operating income in USD in the fiscal year 2022?",
            "output_type": "structured",
            "output_schema": "{\"properties\": {\"company\": {\"description\": \"Company name\",\"type\": \"string\"},\"fiscalYear\": {\"description\": \"The fiscal year for the reported data\",\"type\": \"string\"},\"operatingIncome\": {\"description\": \"Microsoft's operating income in USD\",\"type\": \"number\"},\"revenue\": {\"description\": \"Microsoft's revenue in USD\",\"type\": \"number\"}},\"type\": \"object\"}", 
            "depth": None,
        },
    ]
    expected_outcomes = [(True, True), (True, True), (True, True)]
    outcomes = []
    for t in test_inputs:
        dt = SearchInput.model_validate_json(json.dumps(t))
        try:
            response = monitored_client.search(dt)
        except Exception as e:
            outcomes.append((None, None))
        else:
            try:
                outputdata = monitored_client.postgres_client.pull_data(data = SelectDatabaseData(created_at=None, status_code=None, output_type=None, query=dt.query, search_type=None, limit=None))
            except Exception as e:
                if dt.output_type == "searchResults":
                    outcomes.append((isinstance(response, LinkupSearchResults), None))
                elif dt.output_type == "sourcedAnswer":
                    outcomes.append((isinstance(response, LinkupSourcedAnswer), None))
                else:
                    truth = isinstance(response, BaseModel) or isinstance(response, dict) or isinstance(response, dict)
                    outcomes.append((truth, None))
            else:
                if dt.output_type == "searchResults":
                    outcomes.append((isinstance(response, LinkupSearchResults), True))
                elif dt.output_type == "sourcedAnswer":
                    outcomes.append((isinstance(response, LinkupSourcedAnswer), True))
                else:
                    truth = isinstance(response, BaseModel) or isinstance(response, dict) or isinstance(response, dict)
                    outcomes.append((truth, True))
    assert outcomes == expected_outcomes 