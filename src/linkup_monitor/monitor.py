from linkup import LinkupClient
from postgres_client import PostgresClient
from add_types import SearchInput, InputDatabaseData, SelectDatabaseData, Optional, json, IgnoredFieldWarning, warnings
from typing import Literal
import time
import uuid
import pandas as pd

class MonitoredLinkupClient:
    def __init__(self, linkup_client: LinkupClient, postgres_client: PostgresClient):
        self.linkup_client = linkup_client
        self.postgres_client = postgres_client
    def search(self, data: SearchInput):
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