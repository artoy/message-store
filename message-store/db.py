import os

import sqlalchemy
from google.cloud.sql.connector import Connector

connector = Connector()


def get_conn():
    conn = connector.connect(
        os.environ.get("INSTANCE_CONNECTION_NAME"),
        "pymysql",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        db=os.environ.get("DB_NAME")
    )
    return conn


def setup():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=get_conn
    )

    return pool


def close():
    connector.close()


def insert_message(pool, m):
    with pool.connect() as db_conn:
        sql = sqlalchemy.text(
            "INSERT INTO messages (id, channel_id, user, text, timestamp) VALUES (:id, :channel_id, :user, :text, :timestamp)"
        )
        db_conn.execute(sql, parameters={
            "id": m.id,
            "channel_id": m.channel_id,
            "user": m.user,
            "text": m.text,
            "timestamp": m.timestamp
        })
        db_conn.commit()
