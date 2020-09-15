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
    if "commentid" not in form:
        printError("Comment ID not given")

    commentIDs = form["commentid"].value
    if not commentIDs.isdigit():
        printError("Comment ID must be digit")
        return
    commentID = int(commentIDs)
    cursor.execute("SELECT commenter, topicid FROM comments WHERE id=?", (commentID,))
    commentInfo = cursor.fetchone()
    if commentInfo == None:
        printError("Comment with that ID not found")
        return
    commenter = commentInfo[0]

    username, admin = sessions.getSession(conn, cursor)
    if not admin and username != commenter:
        printError("You're not logged into an admin account and you are trying to delete someone else's comment (you can't do that)")
        return

    cursor.execute("DELETE FROM comments WHERE id=?", (commentID,))

    conn.commit()

    print("Location: topic.py?topic=" + str(commentInfo[1]) + "\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
