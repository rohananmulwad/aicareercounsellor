from utils import loadQueries, handleError
from .connection import getConnection, releaseConnection

Queries = loadQueries("db/queries.sql")


def runQuery(query_name, params=None, commit=False, fetchone=False, fetchall=False):
    """
        Generic query runner.
        - query_name: key from QUERIES dict
        - params: tuple of parameters for the query
        - commit: if True, commits the transaction
        - fetchone: return single row
        - fetchall: return all rows
    """
    sql = Queries.get(query_name)
    print(f'user db creater query {sql}')
    
    if not sql:
        raise ValueError(f"Query {query_name} not found in queries.sql")
    
    conn = getConnection()
    
    try:
        with conn.cursor() as curr:
            curr.execute(sql, params)
            if commit:
                conn.commit()
            if fetchone:
                return curr.fetchone()
            if fetchall:
                return curr.fetchall()
    finally:
        releaseConnection(conn)


@handleError("Fail to create table", internal_error=1)
def createTable(query_name):
    """create user table"""
    return runQuery(query_name, commit=True)



@handleError("Fail to fecth userData", internal_error=1)
def getUser(userName):
    return runQuery("select_user_by_username", params=(userName,), fetchone=True)


@handleError("Fail to insert userData", internal_error=1)
def insertUser(userName, email, passwordHash):
    return runQuery("insert_user", params=(userName, email, passwordHash),
                    commit=True, fetchone=True)


@handleError("Fail to fecth all userData", internal_error=1)
def getAllUsers():
    return runQuery("get_all_user", fetchone=True)


@handleError("Fail to fecth user by email", internal_error=1)
def getUserEmail():
    return runQuery("select_user_by_email", fetchone=True)



