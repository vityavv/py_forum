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
    requiredFields = ["topicname", "topicbody", "categoryid"]
    for field in requiredFields:
        if field not in form:
            printError("Missing form value: " + field)
            return

    categoryIDs = form["categoryid"].value
    if not categoryIDs.isdigit():
        printError("Category ID must be digit")
        return
    categoryID = int(categoryIDs)
    cursor.execute("SELECT * FROM categories WHERE id=?", (categoryID,))
    if cursor.fetchone() == None:
        printError("Category with that ID not found")
        return

    username, _ = sessions.getSession(conn, cursor)
    if not username:
        printError("Not logged in!")
        return

    cursor.execute("INSERT INTO topics (creator, categoryid, name, body) VALUES (?, ?, ?, ?)", (html.escape(html.unescape(username)), categoryID, html.escape(html.unescape(form["topicname"].value)), html.escape(html.unescape(form["topicbody"].value))))

    conn.commit()

    cursor.execute("SELECT id FROM topics ORDER BY id DESC")
    print("Location: topic.py?topic=" + str(cursor.fetchone()[0]) + "\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
