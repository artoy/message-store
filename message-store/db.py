import os

import sqlalchemy
from google.cloud.sql.connector import IPTypes, Connector


def connect():
    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    connector = Connector(ip_type)

    gcp_conn = connector.connect(
        os.environ.get("INSTANCE_CONNECTION_NAME"),
        "pymysql",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        db=os.environ.get("DB_NAME")
    )

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=gcp_conn,
    )

    return gcp_conn, pool.connect()


def close(gcp_conn, db_conn):
    gcp_conn.close()
    db_conn.close()


def insert_message(db_conn, m):
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
