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

    queriedUsername = form["user"].value
    cursor.execute("SELECT username FROM users WHERE username=?", (queriedUsername,))
    test = cursor.fetchone()
    if test == None:
        printError("<h1>404: User not found</h1>")
        return
    username, admin = sessions.getSession(conn, cursor)
    print("Content-Type: text/html\n")
    buildHeader(username, admin)
    print("<main><h1>User info for %s</h1>" % queriedUsername)
    print("<h2>Posts</h2><div class='elements'>")

    for row in cursor.execute("SELECT topics.id, topics.name, topics.categoryid, categories.name FROM topics INNER JOIN categories ON topics.categoryid=categories.id WHERE topics.creator=?", (queriedUsername,)):
        print("<div class='element'><a href='topic.py?topic=%s'>%s</a> <span>in category <a href='category.py?category=%d'>%s</a></span></div>" % row)

    print("</div><h2>Comments</h2><div class='elements'>")

    for row in cursor.execute("SELECT comments.comment, comments.topicid, topics.name, topics.categoryid, categories.name FROM comments INNER JOIN topics ON comments.topicid=topics.id INNER JOIN categories ON topics.categoryid=categories.id WHERE comments.commenter=?", (queriedUsername,)):
        print("<div class='element'>%s <span>on <a href='topic.py?topic=%s'>%s</a> in category <a href='category.py?category=%d'>%s</a></span></div>" % row)

    print("""</div></main></body></html>""")

form = cgi.FieldStorage()
if "user" not in form:
    print("Location: index.py\n")
else:
    try:
        main()
    except:
        print("Content-Type: text/html\n")
        raise
