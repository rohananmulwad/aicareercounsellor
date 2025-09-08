import os 
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

dbUrl = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")


def createDatabase():
    #create's database table if not exists
    conn = psycopg2.connect(dbUrl.replace(dbName, "postgres"))
    conn.autocommit = True
    
    with conn.cursor() as curr:
        curr.execute("SELECT 1 FROM pg_database WHERE datname=%s", (dbName,))
        exists = curr.fetchone()
        if not exists:
            curr.execute(f"CREATE DATABASE {dbName};")
            print(f"[INFO] database {dbName} created")
        else:
            print(f"[INFO] database {dbName} already exists")
    conn.close()


createDatabase()

dbPool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=dbUrl
)


if not dbPool:
    # If pool creation failed, raise error to prevent app from starting
    raise RuntimeError("Failed to initialize database connection pool. Exiting app.")


def getConnection():
    return dbPool.getconn()


def releaseConnection(conn):
    return dbPool.putconn(conn)
