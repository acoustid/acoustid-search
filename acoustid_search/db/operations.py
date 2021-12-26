from typing import Any

from sqlalchemy import sql
from sqlalchemy.sql import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection as DatabaseConnection

from acoustid_search.db.schema import catalog_table


async def get_catalog(db: DatabaseConnection, catalog_name: str) -> Any:
    """
    Create a catalog on the database.

    :param db: Database connection
    :param catalog_name: Name of the catalog
    """
    select_stmt = select([catalog_table]).where(catalog_table.c.name == catalog_name)
    result = await db.execute(select_stmt)
    return result.first()


async def create_catalog(db: DatabaseConnection, catalog_name: str) -> None:
    """
    Create a catalog on the database.

    :param db: Database connection
    :param catalog_name: Name of the catalog
    """
    upsert_stmt = (
        insert(catalog_table)
        .values({catalog_table.c.name: catalog_name})
        .on_conflict_do_update(
            index_elements=[catalog_table.c.name],
            set_={
                catalog_table.c.last_modified_at: sql.func.now(),
            },
        )
    )
    await db.execute(upsert_stmt)


async def delete_catalog(db: DatabaseConnection, catalog_name: str) -> None:
    """
    Delete a catalog from the database.

    :param db: Database connection
    :param catalog_name: Name of the catalog
    """
    delete_stmt = delete(catalog_table).where(catalog_table.c.name == catalog_name)
    await db.execute(delete_stmt)
