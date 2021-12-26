from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    LargeBinary,
    ForeignKey,
    UniqueConstraint,
    sql,
)


metadata = MetaData()

catalog_table = Table(
    "catalog",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=sql.func.now()),
    Column("last_modified_at", DateTime(timezone=True), nullable=False, server_default=sql.func.now()),
    UniqueConstraint("name"),
)

fingerprint = Table(
    "fingerprint",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("catalog_id", Integer, ForeignKey("catalog.id"), nullable=False),
    Column("name", String, nullable=False),
    Column("data", LargeBinary, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=sql.func.now()),
    Column("last_modified_at", DateTime(timezone=True), nullable=False, server_default=sql.func.now()),
    UniqueConstraint("catalog_id", "name"),
)
