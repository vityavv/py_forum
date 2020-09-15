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
    requiredFields = ["topicid", "comment"]
    for field in requiredFields:
        if field not in form:
            printError("Missing form value: " + field)
            return

    topicIDs = form["topicid"].value
    if not topicIDs.isdigit():
        printError("Topic ID must be digit")
        return
    topicID = int(topicIDs)
    cursor.execute("SELECT * FROM topics WHERE id=?", (topicID,))
    if cursor.fetchone() == None:
        printError("Topic with that ID not found")
        return

    username, _ = sessions.getSession(conn, cursor)
    if not username:
        printError("Not logged in!")
        return

    cursor.execute("INSERT INTO comments (commenter, comment, topicid) VALUES (?, ?, ?)", (html.escape(html.unescape(username)), html.escape(html.unescape(form["comment"].value)), topicID))

    conn.commit()

    print("Location: topic.py?topic=" + str(topicID) + "\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
