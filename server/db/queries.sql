-- uuid_extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- vector_extension
CREATE EXTENSION IF NOT EXISTS vector;


-- create_user_table
CREATE TABLE IF NOT EXISTS users(
    userId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userName VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwordHash TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- create_chat_table
CREATE TABLE IF NOT EXISTS chats(
    chatId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userId INT NOT NULL,
    messageData TEXT NOT NULL,
    messageVector vector(1536),
    chatRole ENUM('user','assistant') NOT NULL, 
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

-- get_all_user
SELECT * FROM users ORDER BY createdAt DESC;

-- select_user_by_email
SELECT userId,userName,email,passwordHash,createdAt FROM users
WHERE email=%s

-- select_chats
SELECT chatId, messageData, chatRole, createdAt
FROM chats
WHERE userId = %s
ORDER BY messageVector <-> %s
LIMIT 10;
