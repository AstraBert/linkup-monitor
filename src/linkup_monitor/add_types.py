from pydantic import BaseModel, model_validator
from typing_extensions import Self, Optional
import json
from json import JSONDecodeError
import warnings

class IgnoredFieldWarning(Warning):
    """Throw this when you ignore a field because of some conditions"""

class SearchInput(BaseModel):
    """A Pydantic model for validating and processing search input parameters.

    This class validates and processes search-related parameters, ensuring they meet specific criteria and maintaining data consistency.

    Attributes:
        query (str): The search query string.
        output_type (Optional[str]): Type of output format. Must be one of: 'searchResults', 'sourcedAnswer', 
            or 'structured'. Defaults to 'searchResults'.
        output_schema (Optional[str]): JSON schema string required when output_type is 'structured'.
        depth (Optional[str]): Depth of the search. Must be either 'standard' or 'deep'. 
            Defaults to 'standard'.

    Raises:
        ValueError: If output_type is invalid, if depth is invalid, or if output_schema is missing
            or invalid when output_type is 'structured'.

    Warnings:
        IgnoredFieldWarning: If output_schema is provided but output_type is not 'structured'.

    Example:
        >>> search = SearchInput(
        ...     query="example search",
        ...     output_type="structured",
        ...     output_schema='{"type": "object"}',
        ...     depth="standard"
        ... )
    """
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
    """
    A Pydantic model representing input data for database operations.

    This class validates and processes database-related input data, ensuring data
    consistency and format requirements are met.

    Attributes:
        call_id (str): 36-characters unique identifier for the API call.
        status_code (int): HTTP status code of the response.
        query (str): web search query string.
        output_type (str): Type of output format. Must be one of: 'searchResults', 'sourcedAnswer', or 'structured'.
        search_type (str): Type of search performed. Must be one of: 'standard' or 'deep'.
        duration (float): Time duration of the operation in seconds.

    Raises:
        ValueError: If output_type or search_type contains invalid values.

    Example:
        >>> data = InputDatabaseData(
        ...     call_id=str(uuid.uuid4()),
        ...     status_code=200,
        ...     query="Who was the first Italian president?",
        ...     output_type="searchResults",
        ...     search_type="standard",
        ...     duration=1.5
        ... )
    """
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
    """A Pydantic model for selecting data from a database with validation rules.

    This class inherits from BaseModel and provides field validation for database queries.

    Attributes:
        created_at (Optional[bool]): Flag to order by creation timestamp the data selected from the database: set to None if you don't want any time ordering, set to True if you want descending time ordering and to False if you want ascending time ordering. 
        status_code (Optional[int]): Filter for status code
        output_type (Optional[str]): Filter for type of output format. Must be one of: 'searchResults', 'sourcedAnswer', 'structured'
        query (Optional[str]): Filter for query.
        search_type (Optional[str]): Filter for search type to perform. Must be one of: 'standard', 'deep'
        limit (Optional[int]): Maximum number of results to return

    Raises:
        ValueError: If output_type or search_type contains invalid values

    Example:
        >>> select_data = SelectDatabaseData(
        ...     output_type='searchResults',
        ...     search_type='standard',
        ...     query=None,
        ...     status_code=200,
        ...     limit = None,
        ...     created_at = False,
        ... )
    """
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
        if self.query is not None:
            self.query = self.query.replace("'", "''")
        return self

class OutputDatabaseData(BaseModel):
    """Class representing structured output data for database operations.

    This class inherits from BaseModel and defines the schema for storing API call results
    and database query information.

    Attributes:
        identifier (int): Unique identifier for the database record
        timestamp (str): Timestamp when the database operation occurred
        call_id (str): Unique identifier for the API call
        status_code (int): HTTP status code of the response
        query (str): The web search query query that was executed
        output_type (str): Type of output produced by the query
        search_type (str): Type of search operation performed
        duration (float): Time taken to execute the web search operation in seconds
    """
    identifier: int
    timestamp: str
    call_id: str
    status_code: int
    query: str
    output_type: str
    search_type: str
    duration: float