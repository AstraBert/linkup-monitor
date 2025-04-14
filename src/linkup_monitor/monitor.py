from linkup import LinkupClient
from postgres_client import PostgresClient
from add_types import SearchInput, InputDatabaseData, SelectDatabaseData, Optional, json, IgnoredFieldWarning, warnings
from typing import Literal
import time
import uuid
import pandas as pd

class MonitoredLinkupClient:
    """A wrapper class for LinkupClient that monitors and logs search operations.

    This class extends the functionality of LinkupClient by adding monitoring capabilities,
    logging search operations to a PostgreSQL database, and providing methods to retrieve
    the logged data in various formats.

    Args:
        linkup_client (LinkupClient): The base LinkupClient instance to be monitored.
        postgres_client (PostgresClient): Client for PostgreSQL database operations.

    Attributes:
        linkup_client (LinkupClient): The wrapped LinkupClient instance.
        postgres_client (PostgresClient): Client for database operations.

    Methods:
        search(data: SearchInput): 
            Performs a synchronous search operation and logs the results.
            
        asearch(data: SearchInput): 
            Performs an asynchronous search operation and logs the results.
            
        get_data(data: Optional[SelectDatabaseData], return_mode: str, save_to_file: bool):
            Retrieves logged data from the database in various formats.
    """
    def __init__(self, linkup_client: LinkupClient, postgres_client: PostgresClient):
        self.linkup_client = linkup_client
        self.postgres_client = postgres_client
    def search(self, data: SearchInput):
        """
        Performs a search operation using LinkUp API and logs the request details.

        This method executes a search query through the LinkUp client and stores metadata
        about the request in a PostgreSQL database. It handles both structured and 
        unstructured output types.

        Args:
            data (SearchInput): A SearchInput object containing:
                - query (str): The search query to execute
                - depth (str): The search depth parameter
                - output_type (str): The type of output
                - output_schema (dict, optional): Schema for structured output

        Returns:
            Any: The search results from the LinkUp API

        Raises:
            Exception: Any exception from the LinkUp API call is caught and logged
            with a 500 status code

        Notes:
            - All searches are logged to the database with a unique call_id
            - Failed searches are logged with duration = -1 and status_code = 500
            - Successful searches include the actual duration and status_code = 200
        """
        if data.output_type != "structured":
            try:
                start = time.time()
                response = self.linkup_client.search(query = data.query, depth= 
            data.depth, output_type = data.output_type)
                end = time.time()
                duration = end - start 
                status_code = 200
            except Exception as e:
                duration = -1
                status_code = 500
            result = InputDatabaseData(call_id=str(uuid.uuid4()), status_code=status_code, query = data.query, output_type= data.output_type, search_type = data.depth, duration = duration)
            self.postgres_client.push_data(result)
            return response
        else:
            try:
                start = time.time()
                response = self.linkup_client.search(query = data.query, depth= 
            data.depth, output_type = data.output_type, structured_output_schema= data.output_schema)
                end = time.time()
                duration = end - start 
                status_code = 200
            except Exception as e:
                duration = -1
                status_code = 500
            result = InputDatabaseData(call_id=str(uuid.uuid4()), status_code=status_code, query = data.query, output_type= data.output_type, search_type = data.depth, duration = duration)
            self.postgres_client.push_data(result)
            return response
    async def asearch(self, data: SearchInput):
        """
        Performs an asynchronous search operation using LinkUp API and logs the request details.

        This asynchronous method executes a search query through the LinkUp client and stores metadata
        about the request in a PostgreSQL database. It handles both structured and 
        unstructured output types.

        Args:
            data (SearchInput): A SearchInput object containing:
                - query (str): The search query to execute
                - depth (str): The search depth parameter
                - output_type (str): The type of output
                - output_schema (dict, optional): Schema for structured output

        Returns:
            Any: The search results from the LinkUp API

        Raises:
            Exception: Any exception from the LinkUp API call is caught and logged
            with a 500 status code

        Notes:
            - All searches are logged to the database with a unique call_id
            - Failed searches are logged with duration = -1 and status_code = 500
            - Successful searches include the actual duration and status_code = 200
        """
        if data.output_type != "structured":
            try:
                start = time.time()
                response = await self.linkup_client.async_search(query = data.query, depth= 
            data.depth, output_type = data.output_type)
                end = time.time()
                duration = end - start 
                status_code = 200
            except Exception as e:
                duration = -1
                status_code = 500
            result = InputDatabaseData(call_id=str(uuid.uuid4()), status_code=status_code, query = data.query, output_type= data.output_type, search_type = data.depth, duration = duration)
            self.postgres_client.push_data(result)
            return response
        else:
            try:
                start = time.time()
                response = await self.linkup_client.async_search(query = data.query, depth= 
            data.depth, output_type = data.output_type, structured_output_schema= data.output_schema)
                end = time.time()
                duration = end - start 
                status_code = 200
            except Exception as e:
                duration = -1
                status_code = 500
            result = InputDatabaseData(call_id=str(uuid.uuid4()), status_code=status_code, query = data.query, output_type= data.output_type, search_type = data.depth, duration = duration)
            self.postgres_client.push_data(result)
            return response
    def get_data(self, data: Optional[SelectDatabaseData] = None, return_mode: Literal["json", "pandas", "raw"] = "json", save_to_file: bool = False):
        """
        Retrieves data from the database and returns it in the specified format.

        Args:
            data (SelectDatabaseData, optional): Query parameters for data selection. Defaults to None.
            return_mode (Literal["json", "pandas", "raw"]): Format for the returned data. Options are:
                - "json": Returns data as a list of dictionaries
                - "pandas": Returns data as a pandas DataFrame
                - "raw": Returns raw data objects
                Defaults to "json".
            save_to_file (bool): If True, saves the output to a file. For "json" mode saves as .json, for "pandas" mode saves as .csv. Ignored for "raw" mode. Defaults to False.

        Returns:
            Union[List[dict], pd.DataFrame, List[object]]: Data in the specified format:
                - List[dict] when return_mode="json"
                - pd.DataFrame when return_mode="pandas" 
                - List[object] when return_mode="raw"

        Raises:
            ValueError: If an unsupported return_mode is specified
            IgnoredFieldWarning: If save_to_file=True is used with return_mode="raw"
        """
        output_data = self.postgres_client.pull_data(data)  
        if return_mode == "json":
            ser = [d.model_dump() for d in output_data]
            if save_to_file:
                t = str(time.time()).replace(".","")+"_linkup_monitoring.json"
                with open(t, "w") as f:
                    json.dump(t, f)
                f.close()
            return ser
        elif return_mode == "pandas":
            df = pd.DataFrame([d.model_dump() for d in output_data])
            if save_to_file:
                t = str(time.time()).replace(".","")+"_linkup_monitoring.csv"
                df.to_csv(t, index=False)                
            return df
        elif return_mode == "raw":
            if save_to_file:
                warnings.warn("return_mode is set to 'raw', so the 'save_to_file' parameter will be ignored", IgnoredFieldWarning)
            return output_data
        else:
            raise ValueError(f"return_mode {return_mode} not supported")