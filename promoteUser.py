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
        printError("You're not logged into an admin account, so you can't promote a user account")
        return

    cursor.execute("UPDATE users SET admin=1 WHERE username=?", (username,))

    conn.commit()

    print("Location: admin.py\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
