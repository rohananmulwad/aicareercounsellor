--Enable the uuid-ossp extenson (only once)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- create_users_table
CREATE TABLE IF NOT EXISTS users{
    userId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userName VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwordHash TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
};

--