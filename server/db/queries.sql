-- uuid_extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- vector_extension
CREATE EXTENSION IF NOT EXISTS vector;

-- create_type_role
DROP TYPE IF EXISTS chat_roles;
CREATE TYPE chat_roles AS ENUM('user','assistant')

-- create_user_table
CREATE TABLE IF NOT EXISTS users(
    userId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userName VARCHAR(50)  NOT NULL,
    email VARCHAR(100) NOT NULL,
    passwordHash TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_email UNIQUE (userName, email) 
);

-- alter_chat_table_vecotr
ALTER TABLE chats ALTER COLUMN messageVector TYPE VECTOR(768);

-- create_chat_table
CREATE TABLE IF NOT EXISTS chats(
    chatId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userId UUID NOT NULL,
    messageData TEXT NOT NULL,
    messageVector vector(786),
    chatRole chat_roles NOT NULL, 
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(userId) on DELETE CASCADE 
);

-- select_user_by_username
SELECT userId,userName,email,passwordHash,createdAt FROM users
WHERE userName=%s 

-- insert_user
INSERT INTO users(userName,email,passwordHash) 
VALUES(%s,%s,%s)
ON CONFLICT (userName, email) DO NOTHING
RETURNING userId;

-- insert_chat
INSERT INTO chats(userId,messageData,messageVector,chatRole) VALUES %s

-- get_all_user
SELECT * FROM users ORDER BY createdAt DESC;

-- select_user_by_email
SELECT userId,userName,email,passwordHash,createdAt FROM users
WHERE email=%s

-- select_chats
SELECT chatId, messageData, chatRole, createdAt
FROM chats
WHERE userId = %s
ORDER BY createdAt DESC
LIMIT 10

-- select_chat_vector
SELECT chatId, messageData, chatRole, createdAt
FROM chats
WHERE userId = %s
ORDER BY messageVector <-> %s
LIMIT 10;

-- select_Assement
SELECT assId,assData,createdAt
FROM assigment
WHERE userId=%s 

