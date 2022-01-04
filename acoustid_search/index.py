from typing import List, Dict, Any, NamedTuple, Optional

from aiohttp import ClientSession


class IndexSearchResult(NamedTuple):
    doc_id: int
    score: int


class IndexClient:
    def __init__(self, base_url):
        self.session = ClientSession(base_url)

    async def get_index(self, index_name: str):
        async with self.session.get(f'/{index_name}') as response:
            return await response.json()

    async def create_index(self, index_name: str) -> None:
        async with self.session.put(f'/{index_name}') as response:
            await response.json()

    async def delete_index(self, index_name: str) -> None:
        async with self.session.put(f'/{index_name}') as response:
            await response.json()

    async def get_document(self, index_name: str, doc_id: int) -> None:
        async with self.session.get(f'/{index_name}/_doc/{doc_id}') as response:
            return await response.json()

    async def create_or_update_document(self, index_name: str, doc_id: int, terms: List[int]) -> None:
        payload = {"terms": terms}
        async with self.session.put(f'/{index_name}/_doc/{doc_id}', json=payload) as response:
            return await response.json()

    async def delete_document(self, index_name: str, doc_id: int) -> None:
        async with self.session.delete(f'/{index_name}/_doc/{doc_id}') as response:
            return await response.json()

    async def bulk_update(self, index_name: str, operations: List[Dict[str, Any]]) -> None:
        payload = {"operations": operations}
        async with self.session.post(f'/{index_name}/_bulk', json=payload) as response:
            return await response.json()

    async def search(self, index_name: str, terms: List[int], timeout: Optional[float] = None) -> List[IndexSearchResult]:
        payload = {"terms": terms}
        async with self.session.post(f'/{index_name}/_search', json=payload) as response:
            doc = await response.json()
            return [IndexSearchResult(doc_id=doc['id'], score=doc['score']) for doc in doc['results']]
