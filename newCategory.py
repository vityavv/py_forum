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
    requiredFields = ["categoryname", "categorydesc"]
    for field in requiredFields:
        if field not in form:
            printError("Missing form value: " + field)
            return

    _, admin = sessions.getSession(conn, cursor)
    if not admin:
        printError("You are not logged into an admin account so you cannot create a new category")
        return
    
    cursor.execute("INSERT INTO categories (name, desc) VALUES (?, ?)", (html.escape(html.unescape(form["categoryname"].value)), html.escape(html.unescape(form["categorydesc"].value))))

    conn.commit()

    print("Location: admin.py\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
