from pgsql import Connection
try:
    from add_types import InputDatabaseData, SelectDatabaseData, OutputDatabaseData
except ImportError:
    from .add_types import InputDatabaseData, SelectDatabaseData, OutputDatabaseData
from typing import List, Optional

class PostgresClient:
    """PostgreSQL client for managing linkup monitor data.

    This class provides functionality to interact with a PostgreSQL database for storing and 
    retrieving monitoring data. It handles the creation of necessary tables and provides 
    methods for data insertion and retrieval.

    Attributes:
        connection: A database connection object to interact with PostgreSQL.

    Methods:
        push_data(data): Inserts monitoring data into the database.
        pull_data(data): Retrieves monitoring data from the database based on optional filters.
        
    Args:
        host (str): The hostname where the PostgreSQL server is running.
        port (int): The port number where the PostgreSQL server is listening.
        user (str, optional): The username for database authentication. Defaults to "postgres".
        password (str | None, optional): The password for database authentication. Defaults to None.
        database (str, optional): The name of the database to connect to. Defaults to "postgres".
    """
    def __init__(self, host: str, port: int, user: str = "postgres", password: str | None = None, database: str = "postgres") -> None:
        self.connection = Connection(address=(host, port), user=user, password=password, database=database)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS linkup_monitor (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT NOW(),
                call_id VARCHAR(36) DEFAULT NULL,
                status_code INT DEFAULT NULL,
                duration FLOAT DEFAULT NULL,
                query TEXT DEFAULT NULL,
                output_type TEXT DEFAULT NULL,
                search_type TEXT DEFAULT NULL
            );
            """
        )
    def push_data(self, data: InputDatabaseData) -> None:
        """
        Push data into the linkup_monitor table in the database.

        Args:
            data (InputDatabaseData): Data object containing the following fields:
                - call_id: Unique identifier for the API call
                - status_code: HTTP status code of the response
                - duration: Time taken for the API call in milliseconds
                - query: The search query string
                - output_type: Type of output requested
                - search_type: Type of search performed

        Returns:
            None
        """
        self.connection.execute(f"INSERT INTO linkup_monitor (call_id, status_code, duration, query, output_type, search_type) VALUES ('{data.call_id}', {data.status_code}, {data.duration}, '{data.query}', '{data.output_type}', '{data.search_type}');") 
    def pull_data(self, data: Optional[SelectDatabaseData] = None) -> List[OutputDatabaseData]:
        """Pull data from linkup_monitor table based on optional filter criteria.

        This method retrieves records from the linkup_monitor table. If no filter data is provided,
        it returns all records. When filter criteria are specified, it constructs and executes
        a SQL query with the appropriate WHERE, ORDER BY, and LIMIT clauses.

        Args:
            data (Optional[SelectDatabaseData]): Filter criteria for the query. Can include:
                - Database field values for WHERE conditions
                - created_at (bool): If provided, determines sort order (True=DESC, False=ASC)
                - limit (int): Maximum number of records to return

        Returns:
            List[OutputDatabaseData]: List of database records converted to OutputDatabaseData objects.
                Each object contains:
                - identifier: Record ID
                - timestamp: Creation timestamp
                - call_id: Call identifier
                - query: Query string
                - output_type: Type of output
                - search_type: Type of search
                - duration: Query duration
                - status_code: Response status code
        """
        output: List[OutputDatabaseData] = []
        if data is None:
            selected = self.connection("SELECT * FROM linkup_monitor;")
            for el in selected:
                output.append(OutputDatabaseData(identifier=el.id, timestamp=el.created_at, call_id=el.call_id, query=el.query, output_type=el.output_type, search_type=el.search_type, duration = el.duration, status_code=el.status_code))
        else:
            conditions = data.model_dump()
            fields = {k: v for k,v in conditions.items() if v is not None and k not in ["created_at", "limit"]}
            created_at = conditions.get("created_at", None)
            limit = conditions.get("limit", None)
            if fields != {}:
                conds = [f"{k} = {v}" if not isinstance(v, str) else f"{k} = '{v}'" for k,v in fields.items()]
                if created_at is None and limit is None:
                    selected = self.connection(f"SELECT * FROM linkup_monitor WHERE {' AND '.join(conds)};")
                elif created_at is None and limit is not None:
                    selected = self.connection(f"SELECT * FROM linkup_monitor WHERE {' AND '.join(conds)} LIMIT {limit};")
                elif created_at is not None and limit is None:
                    ordr = "DESC" if created_at else "ASC" 
                    selected = self.connection(f"SELECT * FROM linkup_monitor WHERE {' AND '.join(conds)} ORDER BY created_at {ordr};")
                else:      
                    ordr = "DESC" if created_at else "ASC"   
                    selected = self.connection(f"SELECT * FROM linkup_monitor WHERE {' AND '.join(conds)} ORDER BY created_at {ordr} LIMIT {limit};")
            else:
                if created_at is None and limit is not None:
                    selected = self.connection(f"SELECT * FROM linkup_monitor LIMIT {limit};")
                elif created_at is not None and limit is None:
                    ordr = "DESC" if created_at else "ASC"   
                    selected = self.connection(f"SELECT * FROM linkup_monitor ORDER BY created_at {ordr};")
                else:      
                    ordr = "DESC" if created_at else "ASC"   
                    selected = self.connection(f"SELECT * FROM linkup_monitor ORDER BY created_at {ordr} LIMIT {limit};")               
            for el in selected:
                output.append(OutputDatabaseData(identifier=el.id, timestamp=el.created_at, call_id=el.call_id, query=el.query, output_type=el.output_type, search_type=el.search_type, duration = el.duration, status_code=el.status_code))
        return output