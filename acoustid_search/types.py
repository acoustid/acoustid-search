import datetime
from typing import Protocol


class CatalogInfo(Protocol):
    """
    A protocol for objects that contain information about a catalog.
    """

    id: int
    name: str
    created_at: datetime.datetime
    last_modified_at: datetime.datetime
