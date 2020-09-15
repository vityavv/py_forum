import sqlite3
def initDB(cursor):
    # Only gets called if categories doesn't exist but still
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, desc STRING)")
    # Make sure these are HTML-compatible bc there aren't good html escaping libs in the stdlib
    for name, desc in {"Homework Help": "Help for all of your school work", "Clubs": "Catch-all for anyone wanting to talk about clubs", "Banter/Offtopic": "Everything else"}.items():
        cursor.execute("INSERT INTO categories (name, desc) VALUES (?, ?)", (name, desc))
    cursor.execute("CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY AUTOINCREMENT, creator STRING, categoryid INTEGER, name STRING, body STRING)")
    cursor.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, commenter STRING, topicid STRING, comment STRING)")
