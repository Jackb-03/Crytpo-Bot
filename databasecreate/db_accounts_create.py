import sqlite3

conn = sqlite3.connect("database.db")

conn.execute('DROP TABLE IF EXISTS users')

#create table

conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        user_password TEXT NOT NULL,
        user_APIkey TEXT,
        user_APIsecret TEXT
    )
''')

#close db
conn.close()