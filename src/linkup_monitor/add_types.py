from pydantic import BaseModel, model_validator
from typing_extensions import Self, Optional
import json
from json import JSONDecodeError
import warnings

class IgnoredFieldWarning(Warning):
    """Throw this when you ignore a field because of some conditions"""

class SearchInput(BaseModel):
    query: str
    output_type: Optional[str]
    output_schema: Optional[str] 
    depth: Optional[str]
    @model_validator(mode="after")
    def validate_search_data(self) -> Self:
        if self.output_type is not None and self.output_type not in ['searchResults','sourcedAnswer','structured']:
            raise ValueError(f"Output type must be one of {', '.join(['searchResults','sourcedAnswer','structured'])}")
        if self.depth is not None and self.depth not in ['standard', 'deep']:
            raise ValueError(f"Search type must be one of {', '.join(['standard', 'deep'])}")
        if self.output_type == 'structured':
            if self.output_schema is None:
                raise ValueError("You need to define the output schema as a JSON serializable string if you set 'structured' as output_type")
            else:
                try:
                    json.loads(self.output_schema)
                except JSONDecodeError:
                    raise ValueError("You need to define the output schema as a JSON serializable string.")
        if self.output_type != 'structured' and self.output_type is not None and self.output_schema is not None:
            warnings.warn("output_schema is set to a non-null value but output_type is not set to 'structured', so output_schema will be ignored", IgnoredFieldWarning)
        if self.depth is None:
            self.depth = "standard"
        if self.output_type is None:
            self.output_type = "searchResults"
        return self

class InputDatabaseData(BaseModel):
    call_id: str
    status_code: int
    query: str
    output_type: str
    search_type: str
    duration: float
    @model_validator(mode="after")
    def validate_database_data(self) -> Self:
        self.query = self.query.replace("'","''")
        if self.output_type not in ['searchResults','sourcedAnswer','structured']:
            raise ValueError(f"Output type must be one of {', '.join(['searchResults','sourcedAnswer','structured'])}")
        if self.search_type not in ['standard', 'deep']:
            raise ValueError(f"Search type must be one of {', '.join(['standard', 'deep'])}")
        return self
    
class SelectDatabaseData(BaseModel):
    created_at: Optional[bool]
    status_code: Optional[int]
    output_type: Optional[str]
    query: Optional[str]
    search_type: Optional[str]
    limit: Optional[int]
    @model_validator(mode="after")
    def validate_select_data(self) -> Self:
        if self.output_type is not None and self.output_type not in ['searchResults','sourcedAnswer','structured']:
            raise ValueError(f"Output type must be one of {', '.join(['searchResults','sourcedAnswer','structured'])}")
        if self.search_type is not None and self.search_type not in ['standard', 'deep']:
            raise ValueError(f"Search type must be one of {', '.join(['standard', 'deep'])}")
        return self

class OutputDatabaseData(BaseModel):
    identifier: int
    timestamp: str
    call_id: str
    status_code: int
    query: str
    output_type: str
    search_type: str
    duration: float