from utils import loadQueries, handleError
from psycopg2.extras import execute_values
from .connection import getConnection, releaseConnection
import json

Queries = loadQueries("db/queries.sql")

def runQuery(query_name, params=None, commit=False, fetchone=False, 
             fetchall=False, batch=False):
    """
        Generic query runner.
        - query_name: key from QUERIES dict/file
        - params: tuple of parameters for the query
        - commit: if True, commits the transaction
        - fetchone: return single row
        - fetchall: return all rows
    """
    sql = Queries.get(query_name)    
    if not sql:
        raise ValueError(f"Query {query_name} not found in queries.sql")
    
    conn = getConnection()
    
    try:
        with conn.cursor() as curr:
            if batch:
                execute_values(curr, sql, params)
            else:
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
def gernalQuery(query_name):
    """create user table, it's a gernalQuery Runer"""
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
    return runQuery("get_all_user", fetchall=True)


@handleError("Fail to fecth user by email", internal_error=1)
def getUserEmail(email: str):
    return runQuery("select_user_by_email", params=(email,), fetchone=True)


@handleError("Fail to fecth chat data", internal_error=1)
def getChatData(userId: str):
    return runQuery("select_chats", params=(userId,), fetchall=True)

@handleError("Fail to fecth chat data vector", internal_error=1)
def getChatDataByEmbedding(userId: str, messageVector: str):
    return runQuery("select_chat_vector", params=(userId, messageVector), fetchall=True)


@handleError("Fail to insert chat data", internal_error=1)
def insertChatData(data: list):
    return runQuery("insert_chat", params=data, batch=True, commit=True)
    
@handleError("Fail to insert quiz data ", internal_error=1)
def insertQuizData(userId: str, data: list):
    profileData = json.dumps(data)
    return runQuery("insert_quiz", params=(userId, profileData,), commit=True)

@handleError("Fail to fetch quiz data", internal_error=1)
def getQuizData(userId: str):
    return runQuery("select_quiz", params=(userId,), fetchall=True)

 