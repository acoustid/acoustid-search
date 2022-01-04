import time
from typing import List, Optional

from sqlalchemy import sql
from sqlalchemy.ext.asyncio import AsyncEngine as DatabaseEngine, AsyncConnection as DatabaseConnection

from acoustid_search.backend import Backend, SearchResult
from acoustid_search.index import IndexClient
from acoustid_search.legacy.db.schema import fingerprint_table


DEFAULT_SEARCH_TIMEOUT = 10.0
DEFAULT_SEARCH_LIMIT = 100


async def set_statement_timeout(db: DatabaseConnection, timeout: float) -> None:
    """
    Set the statement timeout for the given database connection.

    :param db: Database connection
    :param timeout: Timeout in seconds
    """
    await db.execute("SET LOCAL statement_timeout = %s", (timeout * 1000,))


class DeadlineTimer:

    def __init__(self, timeout: float) -> None:
        self.deadline = time.monotonic() + timeout

    def is_expired(self) -> bool:
        return time.monotonic() > self.deadline

    def remaining_time(self) -> float:
        return self.deadline - time.monotonic()


class LegacySearchBackend(Backend):

    def __init__(self, db: DatabaseEngine, index: IndexClient, catalog_name: str) -> None:
        self.db = db
        self.index = index
        self.index_name = 'main'
        self.catalog_name = catalog_name

    def create_catalog(self, name: str) -> None:
        if name != self.catalog_name:
            raise NotImplementedError(f"Only catalog {self.catalog_name} is supported")

    def delete_catalog(self, name: str) -> None:
        raise NotImplementedError("Deleting catalog is not supported")

    def list_catalogs(self) -> List[str]:
        return [self.catalog_name]

    async def search(self, query: List[int], limit: Optional[int], timeout: Optional[float]) -> List[SearchResult]:
        deadline = DeadlineTimer(timeout or DEFAULT_SEARCH_TIMEOUT)

        async with self.db.connect() as conn:
            await set_statement_timeout(conn, deadline.remaining_time())
            select_stmt = sql.select(sql.func.acoustid_extract_query(query))
            indexed_query = await conn.scalar(select_stmt)

        candidates = await self.index.search(self.index_name, indexed_query, deadline.remaining_time())
        candidate_fingerprint_ids = [c.doc_id for c in candidates]

        results = []
        async with self.db.connect() as conn:
            await set_statement_timeout(conn, deadline.remaining_time())
            select_stmt = (
                sql.select([
                    fingerprint_table.c.id,
                    sql.func.acoustid_compare2(fingerprint_table.c.fingerprint, query).label("score"),
                ])
                .select_from(fingerprint_table)
                .where(fingerprint_table.c.id.in_(candidate_fingerprint_ids))
                .order_by(sql.desc("score"))
                .limit(limit or DEFAULT_SEARCH_LIMIT)
            )
            rows = await conn.execute(select_stmt)
            for row in rows:
                results.append(SearchResult(str(row.id), row.score))
        return results
