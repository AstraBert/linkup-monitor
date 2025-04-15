## linkup_monitor package

### Submodules

#### linkup_monitor.add_types module

This module defines custom types and warnings used within the `linkup_monitor` package.

*   **Classes**
    *   `IgnoredFieldWarning(Warning)`: A custom warning class for when a field is ignored.

        *   Inherits from: `Warning`
        *   Description: A custom warning class for when a field is ignored due to certain conditions.

    *   `SearchInput(BaseModel)`: A Pydantic model for validating and processing search input parameters.

        *   Inherits from: `pydantic.BaseModel`
        *   Description: This class validates and processes search-related parameters, ensuring they meet specific criteria and maintaining data consistency.
        *   Attributes:
            *   `query` (`str`): The search query string.
            *   `output_type` (`Optional[str]`): Type of output format. Must be one of: `'searchResults'`, `'sourcedAnswer'`, or `'structured'`. Defaults to `'searchResults'`.
            *   `output_schema` (`Optional[str]`): JSON schema string required when `output_type` is `'structured'`.
            *   `depth` (`Optional[str]`): Depth of the search. Must be either `'standard'` or `'deep'`. Defaults to `'standard'`.
        *   Raises:
            *   `ValueError`: If `output_type` is invalid, if `depth` is invalid, or if `output_schema` is missing or invalid when `output_type` is `'structured'`.
        *   Warnings:
            *   `IgnoredFieldWarning`: If `output_schema` is provided but `output_type` is not `'structured'`.
        *   Example:

            ```python
            >>> search = SearchInput(
            ...     query="example search",
            ...     output_type="structured",
            ...     output_schema='{"type": "object"}',
            ...     depth="standard"
            ... )
            ```
    *   `InputDatabaseData(BaseModel)`: A Pydantic model representing input data for database operations.
        *   Inherits from: `pydantic.BaseModel`
        *   Description: This class validates and processes database-related input data, ensuring data consistency and format requirements are met.
        *   Attributes:
            *   `call_id` (`str`): 36-characters unique identifier for the API call.
            *   `status_code` (`int`): HTTP status code of the response.
            *   `query` (`str`): web search query string.
            *   `output_type` (`str`): Type of output format. Must be one of: `'searchResults'`, `'sourcedAnswer'`, or `'structured'`.
            *   `search_type` (`str`): Type of search performed. Must be one of: `'standard'` or `'deep'`.
            *   `duration` (`float`): Time duration of the operation in seconds.
        *   Raises:
            *   `ValueError`: If `output_type` or `search_type` contains invalid values.
        *   Example:
            ```python
            >>> data = InputDatabaseData(
            ...     call_id=str(uuid.uuid4()),
            ...     status_code=200,
            ...     query="Who was the first Italian president?",
            ...     output_type="searchResults",
            ...     search_type="standard",
            ...     duration=1.5
            ... )
            ```
    *   `SelectDatabaseData(BaseModel)`: A Pydantic model for selecting data from a database with validation rules.
        *   Inherits from: `pydantic.BaseModel`
        *   Description: This class inherits from BaseModel and provides field validation for database queries.
        *   Attributes:
            *   `created_at` (`Optional[bool]`) Flag to order by creation timestamp the data selected from the database: set to None if you don't want any time ordering, set to True if you want descending time ordering and to False if you want ascending time ordering.
            *   `status_code` (`Optional[int]`) Filter for status code
            *   `output_type` (`Optional[str]`) Filter for type of output format. Must be one of: 'searchResults', 'sourcedAnswer', 'structured'
            *   `query` (`Optional[str]`) Filter for query.
            *   `search_type` (`Optional[str]`) Filter for search type to perform. Must be one of: 'standard', 'deep'
            *   `limit` (`Optional[int]`) Maximum number of results to return
        *   Raises:
            *   `ValueError`: If output_type or search_type contains invalid values
        *   Example:
            ```python
            >>> select_data = SelectDatabaseData(
            ...     output_type='searchResults',
            ...     search_type='standard',
            ...     query=None,
            ...     status_code=200,
            ...     limit = None,
            ...     created_at = False,
            ... )
            ```
    *   `OutputDatabaseData(BaseModel)`: Class representing structured output data for database operations.
        *   Inherits from: `pydantic.BaseModel`
        *   Description: This class inherits from BaseModel and defines the schema for storing API call results and database query information.
        *   Attributes:
            *   `identifier` (`int`): Unique identifier for the database record
            *   `timestamp` (`str`): Timestamp when the database operation occurred
            *   `call_id` (`str`): Unique identifier for the API call
            *   `status_code` (`int`): HTTP status code of the response
            *   `query` (`str`): The web search query query that was executed
            *   `output_type` (`str`): Type of output produced by the query
            *   `search_type` (`str`): Type of search operation performed
            *   `duration` (`float`): Time taken to execute the web search operation in seconds

#### linkup_monitor.postgres_client module

This module defines the [`PostgresClient`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/postgres_client.py) class, which handles interactions with the PostgreSQL database used for storing monitoring data.

*   **Classes**
    *   `PostgresClient(host: str, port: int, user: str = "postgres", password: str | None = None, database: str = "postgres")`: Manages the connection to the PostgreSQL database.
        *   `__init__(host: str, port: int, user: str = "postgres", password: str | None = None, database: str = "postgres")`: Initializes the [`PostgresClient`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/postgres_client.py) with connection details.
            *   Parameters:
                *   `host` (`str`): The hostname where the PostgreSQL server is running.
                *   `port` (`int`): The port number where the PostgreSQL server is listening.
                *   `user` (`str`, optional): The username for database authentication. Defaults to `"postgres"`.
                *   `password` (`str | None`, optional): The password for database authentication. Defaults to `None`.
                *   `database` (`str`, optional): The name of the database to connect to. Defaults to `"postgres"`.
            *   Example:
                ```python
                >>> from postgres_client import PostgresClient
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                ```
        *   `push_data(data: InputDatabaseData) -> None`: Pushes data into the `linkup_monitor` table in the database.
            *   Parameters:
                *   `data` ([`InputDatabaseData`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py)): Data object containing the following fields:
                    *   `call_id` (`str`): Unique identifier for the API call.
                    *   `status_code` (`int`): HTTP status code of the response.
                    *   `duration` (`float`): Time taken for the API call in seconds.
                    *   `query` (`str`): The search query string.
                    *   `output_type` (`str`): Type of output requested.
                    *   `search_type` (`str`): Type of search performed.
            *   Returns:
                *   `None`
            *   Example:
                ```python
                >>> from postgres_client import PostgresClient
                >>> from add_types import InputDatabaseData
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                >>> data = InputDatabaseData(call_id="your_call_id", status_code=200, duration=1.5, query="example query", output_type="searchResults", search_type="standard")
                >>> postgres_client.push_data(data)
                ```
        *   `pull_data(data: Optional[SelectDatabaseData] = None) -> List[OutputDatabaseData]`: Pulls data from `linkup_monitor` table based on optional filter criteria.
            *   Parameters:
                *   `data` (`Optional[SelectDatabaseData]`, defaults to `None`): Filter criteria for the query. Can include:
                    *   Database field values for `WHERE` conditions
                    *   `created_at` (`bool`): If provided, determines sort order (`True`=`DESC`, `False`=`ASC`)
                    *   `limit` (`int`): Maximum number of records to return
            *   Returns:
                *   `List[OutputDatabaseData]`: List of database records converted to [`OutputDatabaseData`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py) objects.
            *   Example:
                ```python
                >>> from postgres_client import PostgresClient
                >>> from add_types import SelectDatabaseData
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                >>> select_data = SelectDatabaseData(
                ...        created_at = False,
                ...        status_code = 200,
                ...        output_type = None,
                ...        query = None,
                ...        search_type = None,
                ...        limit = 100
                ... )
                >>> results = postgres_client.pull_data(select_data)
                ```

#### linkup_monitor.monitor module

This module provides the core functionality for monitoring Linkup searches. It includes the [`SearchInput`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py) data model, and the [`MonitoredLinkupClient`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/monitor.py) class which extends the basic `LinkupClient` to include monitoring capabilities using a PostgreSQL database.

*   **Classes**
    *   `MonitoredLinkupClient(linkup_client, postgres_client)`: Extends the `LinkupClient` to monitor searches.
        *   `__init__(linkup_client: LinkupClient, postgres_client: PostgresClient)`: Initializes the `MonitoredLinkupClient` with a [`LinkupClient`](https://linkup.so) and a [`PostgresClient`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/postgres_client.py).
            *   Parameters:
                *   `linkup_client` ([`LinkupClient`](https://linkup.so)): The Linkup client to use for searches.
                *   `postgres_client` ([`PostgresClient`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/postgres_client.py)): The PostgreSQL client to use for database operations.
        *   `search(data: SearchInput)`: Performs a synchronous search using the [`LinkupClient`](https://linkup.so) and saves the results to the database.
            *   Parameters:
                *   `data` ([`SearchInput`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py)): A [`SearchInput`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py) object containing the search parameters.
            *   Returns:
                *   `Any`: The search results from the LinkUp API.
            *   Raises:
                *   `Exception`: Any exception from the LinkUp API call is caught and logged with a 500 status code.
            *   Example:
                ```python
                >>> from linkup import LinkupClient
                >>> from postgres_client import PostgresClient
                >>> from monitor import MonitoredLinkupClient
                >>> from add_types import SearchInput
                >>> linkup_client = LinkupClient(api_key="YOUR_API_KEY")
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                >>> monitored_client = MonitoredLinkupClient(linkup_client, postgres_client)
                >>> search_data = SearchInput(
                ...        query = "Who won the Nobel Prize for Chemistry in 2023?",
                ...        output_type = "searchResults",
                ...        output_schema = None,
                ...        depth = "deep",
                ... )
                >>> results = monitored_client.search(search_data)
                ```
        *   `asearch(data: SearchInput)`: Performs an asynchronous search using the [`LinkupClient`](https://linkup.so) and saves the results to the database.
            *   Parameters:
                *   `data` ([`SearchInput`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py)): A [`SearchInput`](https://github.com/AstraBert/linkup-client/tree/main/src/linkup_monitor/add_types.py) object containing the search parameters.
            *   Returns:
                *   `Any`: The search results from the LinkUp API.
            *   Raises:
                *   `Exception`: Any exception from the LinkUp API call is caught and logged with a 500 status code.
            *   Example:
                ```python
                >>> import asyncio
                >>> from linkup import LinkupClient
                >>> from postgres_client import PostgresClient
                >>> from monitor import MonitoredLinkupClient
                >>> from add_types import SearchInput
                >>> linkup_client = LinkupClient(api_key="YOUR_API_KEY")
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                >>> monitored_client = MonitoredLinkupClient(linkup_client, postgres_client)
                >>> search_data = SearchInput(
                ...        query = "Who won the Nobel Prize for Chemistry in 2023?",
                ...        output_type = "searchResults",
                ...        output_schema = None,
                ...        depth = "deep",
                ... )
                >>> results = asyncio.run(monitored_client.asearch(search_data))
                ```
        *   `get_data(data: Optional[SelectDatabaseData] = None, return_mode: Literal["json", "pandas", "raw"] = "json", save_to_file: bool = False)`: Retrieves monitoring data from the PostgreSQL database.
            *   Parameters:
                *   `data` (`Optional[SelectDatabaseData]`, defaults to `None`): Query parameters for data selection.
                *   `return_mode` (`Literal["json", "pandas", "raw"]`, defaults to `"json"`): Format for the returned data. Options are:
                    *   `"json"`: Returns data as a list of dictionaries
                    *   `"pandas"`: Returns data as a pandas DataFrame
                    *   `"raw"`: Returns raw data objects
                *   `save_to_file` (`bool`, defaults to `False`): If `True`, saves the output to a file. For `"json"` mode saves as `.json`, for `"pandas"` mode saves as `.csv`. Ignored for `"raw"` mode.
            *   Returns:
                *   `Union[List[dict], pd.DataFrame, List[object]]`: Data in the specified format.
            *   Raises:
                *   `ValueError`: If an unsupported `return_mode` is specified.
                *   `IgnoredFieldWarning`: If `save_to_file=True` is used with `return_mode="raw"`.
            *   Example:
                ```python
                >>> from linkup import LinkupClient
                >>> from postgres_client import PostgresClient
                >>> from monitor import MonitoredLinkupClient
                >>> from add_types import SelectDatabaseData
                >>> linkup_client = LinkupClient(api_key="YOUR_API_KEY")
                >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
                >>> monitored_client = MonitoredLinkupClient(linkup_client, postgres_client)
                >>> select_data = SelectDatabaseData(
                ...        created_at = False,
                ...        status_code = 200,
                ...        output_type = None,
                ...        query = None,
                ...        search_type = None,
                ...        limit = 100
                ... )
                >>> results = monitored_client.get_data(select_data, return_mode="json", save_to_file=False)
                ```
* **Functions**:
    * `monitor(pg_client: PostgresClient)` (decorator):  Decorator that monitors the execution of a function, measures its duration, and logs the input and output data to a PostgreSQL database.
    The decorated function should accept a LinkupClient and a SearchInput object as arguments. It measures the execution time of the function, catches any exceptions that occur, and logs the input data, output type, search type, status code, and duration to the database.
    * `monitored_search(linkup_client: LinkupClient, data: SearchInput)`: Performs a monitored search using the Linkup client.
        
        * **Args**:
            * linkup_client (LinkupClient): The Linkup client to use for the search.
            * data (SearchInput): The search input data.

        * **Returns**:
            * The response from the Linkup client's search method.  The structure of the response depends on the output_type specified in the SearchInput. If output_type is 'structured', the response will conform to the output_schema, if provided.
    
    **Example usage**:
    ```python
    >>> from linkup import LinkupClient
    >>> from postgres_client import PostgresClient
    >>> from monitor import monitor, monitored_search, SearchInput
    >>> linkup_client = LinkupClient(api_key="YOUR_API_KEY")
    >>> postgres_client = PostgresClient(host="localhost", port=5432, database="your_db", user="your_user", password="your_password")
    >>> @monitor(pg_client = postgres_client)
    >>> def search(linkup_client: LinkupClient, data: SearchInput):
    ...     return monitored_search(linkup_client, data)
    ```
    