from psycopg2 import pool
import os 
from dotenv import load_dotenv

load_dotenv()

dbPool=pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=os.getenv("DB_URL")
)


if not dbPool:
    # If pool creation failed, raise error to prevent app from starting
    raise RuntimeError("Failed to initialize database connection pool. Exiting application.")

def getConnection():
    return dbPool.getconn()

def releaseConnection(conn):
    return dbPool.putconn(conn)

