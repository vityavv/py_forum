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
    if "topic" not in form:
        printError("Topic not given")

    topicIDs = form["topic"].value
    if not topicIDs.isdigit():
        printError("Topic ID must be digit")
        return
    topicID = int(topicIDs)
    cursor.execute("SELECT creator, categoryid FROM topics WHERE id=?", (topicID,))
    topicInfo = cursor.fetchone()
    if topicInfo == None:
        printError("Topic with that ID not found")
        return
    creator = topicInfo[0]

    username, admin = sessions.getSession(conn, cursor)
    if not admin and username != creator:
        printError("You're not logged into an admin account and you are trying to delete someone else's topic (you can't do that)")
        return

    cursor.execute("DELETE FROM comments WHERE topicid=?", (topicID,))
    cursor.execute("DELETE FROM topics WHERE id=?", (topicID,))

    conn.commit()

    print("Location: category.py?category=" + str(topicInfo[1]) + "\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
