import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

metadata = sa.MetaData()

track_table = sa.Table(
    "track",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa.sql.func.current_timestamp(), nullable=False),
    sa.Column("updated", sa.DateTime(timezone=True)),
    sa.Column("new_id", sa.Integer, sa.ForeignKey("track.id")),
    sa.Column("gid", pg.UUID, nullable=False),
)

fingerprint_table = sa.Table(
    "fingerprint",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("fingerprint", pg.ARRAY(sa.Integer), nullable=False),
    sa.Column("length", sa.SmallInteger, sa.CheckConstraint("length>0"), nullable=False),
    sa.Column("bitrate", sa.SmallInteger, sa.CheckConstraint("bitrate>0")),
    sa.Column("format_id", sa.Integer),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa.sql.func.current_timestamp(), nullable=False),
    sa.Column("updated", sa.DateTime(timezone=True)),
    sa.Column("track_id", sa.Integer, sa.ForeignKey("track.id"), nullable=False),
    sa.Column("submission_count", sa.Integer, nullable=False),
)
