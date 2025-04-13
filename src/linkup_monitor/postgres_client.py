from pgsql import Connection
from add_types import InputDatabaseData, SelectDatabaseData, OutputDatabaseData
from typing import List, Optional

class PostgresClient:
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
        self.connection.execute(f"INSERT INTO linkup_monitor (call_id, status_code, duration, query, output_type, search_type) VALUES ('{data.call_id}', {data.status_code}, {data.duration}, '{data.query}', '{data.output_type}', '{data.search_type}');") 
    def pull_data(self, data: Optional[SelectDatabaseData] = None) -> List[OutputDatabaseData]:
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