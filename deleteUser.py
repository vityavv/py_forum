#!/usr/bin/python

import cgi
import cgitb
import sqlite3
import html
cgitb.enable()
import sessions

def printError(err):
    print("Content-type: text/html\n")
    print("<h1>" + err + "</h1>")

def main():
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()

    form = cgi.FieldStorage()
    # In other files, I put this by main, but tbh I want to get this over with so I guess this is gonna stay like that.
    if "user" not in form:
        printError("Username not given")
        return

    username = form["user"].value

    _, admin = sessions.getSession(conn, cursor)
    if not admin:
        printError("You're not logged into an admin account, so you can't delete a user account")
        return

    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    #cursor.execute("DELETE comments FROM comments INNER JOIN topics ON comments.topicid=topics.id WHERE topics.categoryid=?", (categoryID,))
    cursor.execute("DELETE FROM comments WHERE commenter=?", (username,))
    cursor.execute("DELETE FROM topics WHERE creator=?", (username,))

    conn.commit()

    print("Location: admin.py\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
