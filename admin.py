#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()
import sqlite3
import initDB
import sessions
from header import buildHeader
from urllib.parse import quote

def printError(err):
    print("Content-Type: text/html\n")
    print("<h1>" + err + "</h1>")

def main():
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone() == None:
        print("Location: index.py\n")
        return

    username, admin = sessions.getSession(conn, cursor)
    if not admin:
        print("Location: index.py\n")
    print("Content-Type: text/html\n")
    buildHeader(username, admin)
    print("""<main><h1>Admin Dashboard</h1>
            <h2>Categories</h2>
            <div class="elements">""")

    for row in cursor.execute("SELECT * FROM categories"):
        print("<div class='element'><a href='category.py?category=%s'>%s</a> <span>%s <a href='deleteCategory.py?category=%s' class='delete'>Delete</a></span></div>" % (row[0], row[1], row[2], row[0]))

    print("""</div>
        <h2>New Category</h2>
        <form action='newCategory.py' method='POST'>
            <label>
                Category name: <input type='text' name='categoryname'/>
            </label><br/>
            <label>
                Category description: <input type='text' name='categorydesc'/>
            </label><br/>
            <button type='submit'>Create Category</button>
        </form></div>
        <h2>Users</h2>
        <div class='elements'>""")

    for row in cursor.execute("SELECT username, admin FROM users"):
        print("<div class='element'><a href='user.py?user=%s'>%s</a><span>" % (quote(row[0]), row[0]))
        if row[1]:
            print("<b>(admin)</b>")
        print("<a href='deleteUser.py?user=%s' class='delete'>Delete</a>" % (quote(row[0]),))
        if row[0] != username:
            print(" | <a href='promoteUser.py?user=%s' class='promote'>Promote</a>" % (quote(row[0]),))
        else:
            print(" (you)")
        print("</span></div>")

    print("""</div></main></body></html>""")

try:
    main()
except:
    print("Content-Type: text/html\n")
    raise
