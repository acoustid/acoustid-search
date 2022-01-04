from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import fnmatch


@dataclass
class SearchResult:
    doc_id: str
    score: float


class Backend(ABC):

    @abstractmethod
    def create_catalog(self, name: str) -> None:
        ...

    @abstractmethod
    def delete_catalog(self, name: str) -> None:
        ...

    @abstractmethod
    def list_catalogs(self) -> List[str]:
        ...

    @abstractmethod
    async def search(self, query: List[int], limit: Optional[int], timeout: Optional[float]) -> List[SearchResult]:
        ...


class UnknownBackend(Exception):
    pass


class BackendRegistry:
    def __init__(self) -> None:
        self.backends: Dict[str, Backend] = {}
        self.routes: List[Tuple[str, str]] = []
        self.default_backend_name: Optional[str] = None

    def backend_names(self) -> List[str]:
        return list(self.backends.keys())

    def register_backend(self, name: str, backend: Backend) -> None:
        self.backends[name] = backend

    def set_default_backend(self, backend_name: str) -> None:
        if backend_name not in self.backends:
            raise UnknownBackend(f"Unknown backend: {backend_name}")
        self.default_backend_name = backend_name

    def route(self, catalog_pattern: str, backend_name: str) -> None:
        if backend_name not in self.backends:
            raise UnknownBackend(f"Unknown backend: {backend_name}")
        self.routes.append((catalog_pattern, backend_name))

    def find_backend(self, catalog_name: str) -> Optional[Backend]:
        for catalog_pattern, backend_name in self.routes:
            if fnmatch.fnmatch(catalog_name, catalog_pattern):
                return self.backends[backend_name]
        if self.default_backend_name is not None:
            return self.backends[self.default_backend_name]
        return None
