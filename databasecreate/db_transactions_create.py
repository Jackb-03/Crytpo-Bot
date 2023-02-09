import sqlite3

# Open and connect to the twitterbot database
conn = sqlite3.connect("database.db")

conn.execute("DROP TABLE IF EXISTS transactions")

# Create details table in the DB
conn.execute('''
    CREATE TABLE transactions (
        transaction_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        tracking_id INTEGER NOT NULL,
        transaction_twitteraccount TEXT NOT NULL,
        transaction_keyword TEXT NOT NULL, 
        transaction_cryptocurrency TEXT NOT NULL,
        transaction_amount INTEGER NOT NULL,
        transaction_bought INTEGER NOT NULL,
        transaction_APIkey TEXT NOT NULL,
        transaction_APIsecret TEXT NOT NULL
    )
''')

# Close database
conn.close()