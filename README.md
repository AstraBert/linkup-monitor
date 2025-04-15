# LinkUp Monitor

## A monitoring solution for world's best search for AI apps.

**`linkup-monitor`** is a python package aimed at providing a monitoring solution for [Linkup](https://linkup.so), a web searching tool that allows you to scrape LLM-friendly answers from the web. `linkup-monitor` exploits PostgreSQL as a backend database and monitors queries, execution times, success status, search type and output type, allowing for a broad control over search analytics.

## Installation and usage

`linkup-monitor` can be installed using `pip` in the following way:

```bash
pip install linkup-monitor
# or, for a faster installation
uv pip install linkup-monitor
```

And is available as in your python script:

- You can **initialize** it:

```python
from linkup_monitor.postgres_client import PostgresClient
from linkup_monitor.monitor import LinkupClient, MonitoredLinkupClient
import os

pg_client = PostgresClient(host='localhost', port=5432, user='postgres', password = 'admin', database = 'postgres') # replace with your Postgres configuration
linkup_client = LinkupClient(api_key=os.getenv('LINKUP_API_KEY')) # assuming you exported LINKUP_API_KEY as an environment variable
monitored_client = MonitoredLinkupClient(linkup_client = linkup_client, postgres_client = pg_client)
```

- **Synchronously** search the web: 

```python
from linkup_monitor.monitor import SearchInput


data = SearchInput(
    query = "Who won the Nobel Prize for Chemistry in 2023?",
    output_type = "searchResults",
    output_schema = None,
    depth = "deep",
)
response = monitored_client.search(data = data)
print(response)
```

- **Asynchronously** search the web:

```python
from linkup_monitor.monitor import SearchInput
import asyncio

async def main():
    data = SearchInput(
        query = "What were Microsoft revenue and operating income in USD in the fiscal year 2022?",
        output_type = "structured",
        output_schema = "{\"properties\": {\"company\": {\"description\": \"Company name\",\"type\": \"string\"},\"fiscalYear\": {\"description\": \"The fiscal year for the reported data\",\"type\": \"string\"},\"operatingIncome\": {\"description\": \"Microsoft's operating income in USD\",\"type\": \"number\"},\"revenue\": {\"description\": \"Microsoft's revenue in USD\",\"type\": \"number\"}},\"type\": \"object\"}",
        depth = "deep",
    )
    response = await monitored_client.asearch(data = data)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

- Get the **monitoring** data:

```python
from linkup_monitor.monitor import SelectDatabaseData
# get raw data without filtering them
output_data = monitored_client.get_data(return_mode="raw")
print(output_data)
# get data in JSON format, save them to a JSON file and filter them by status code, ordering them by ascending timestamp and limiting the returned values to 100
filter_data = SelectDatabaseData(
    created_at = False,
    status_code = 200, # you can also set it to 500, which identifies failed searches
    output_type = None,
    query = None,
    search_type = None,
    limit = 100
)
output_data = monitored_client.get_data(data=filter_data, return_mode="json", save_to_file=True)
print(output_data)
# get data in pd.DataFrame format and save them as a CSV file and filter them by output type, ordering them by descending timestamp
filter_data = SelectDatabaseData(
    created_at = True,
    status_code = None, # you can also set it to 500, which identifies failed searches
    output_type = "sourcedAnswer",
    query = None,
    search_type = None,
    limit = None,
)
output_data = monitored_client.get_data(data=filter_data, return_mode="pandas", save_to_file=True)
print(output_data)
```

- Use the **decorator** for a functional integration:

```python
from linkup import LinkupClient
from linkup_monitor.postgres_client import PostgresClient
from linkup_monitor.monitor import monitor, monitored_search, SearchInput

linkup_client = LinkupClient(api_key="YOUR_API_KEY")
postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")

@monitor(pg_client = postgres_client)
def search(linkup_client: LinkupClient, data: SearchInput):
    return monitored_search(linkup_client, data)
```

You can find a complete reference for the package in [REFERENCE.md](https://github.com/AstraBert/linkup-monitor/tree/main/REFERENCE.md)

### Contributing

Contributions are always welcome!

Find contribution guidelines at [CONTRIBUTING.md](https://github.com/AstraBert/linkup-monitor/tree/main/CONTRIBUTING.md)

### License and Funding

This project is open-source and is provided under an [MIT License](https://github.com/AstraBert/linkup-monitor/tree/main/LICENSE).

If you found it useful, please consider [funding it](https://github.com/sponsors/AstraBert).