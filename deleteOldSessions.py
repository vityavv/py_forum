import sqlite3

conn = sqlite3.connect("../www/forum.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM sessions WHERE age <= datetime('now', '-1 days')")
conn.commit()
