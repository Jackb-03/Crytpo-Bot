import sqlite3

# Open and connect to the twitterbot database
conn = sqlite3.connect("database.db")

conn.execute("DROP TABLE IF EXISTS tracking")



# Create tracking table in the DB
conn.execute('''
    CREATE TABLE tracking (
        user_id INTEGER NOT NULL,
        tracking_id INTEGER PRIMARY KEY,
        tracking_twitteraccount TEXT NOT NULL,
        tracking_keyword TEXT NOT NULL, 
        tracking_cryptocurrency TEXT NOT NULL,
        tracking_amount INTEGER NOT NULL,
        user_APIkey TEXT NOT NULL,
        user_APIsecret TEXT NOT NULL
    )
''')

# Close database
conn.close()