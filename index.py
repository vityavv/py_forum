#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()
import sqlite3
import initDB
import sessions
from header import buildHeader

def printError(err):
    print("<h1>" + err + "</h1>")

def main():
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
    if cursor.fetchone() == None:
        initDB.initDB(cursor)
        conn.commit()
    # Check if logged in
    username, admin = sessions.getSession(conn, cursor)
    print("Content-type: text/html\n")
    buildHeader(username, admin)
    print("<main><h1>Victor's Forum</h1><div class='elements'>")

    for row in cursor.execute("SELECT * FROM categories"):
        print("<div class='element'><a href='category.py?category=%s'>%s</a> %s</div>" % (row[0], row[1], row[2]))

    print("""</div></main></body></html>""")

try:
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
