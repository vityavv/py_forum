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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='comments'")
    if cursor.fetchone() == None:
        initDB.initDB(cursor)
        conn.commit()

    topicIDs = form["topic"].value
    if not topicIDs.isdigit():
        printError("Topic ID must be number")
        return
    topicID = int(topicIDs)
    cursor.execute("SELECT categoryid, creator, name, body FROM topics WHERE id=?", (topicID,))
    topicInfo = cursor.fetchone()
    if topicInfo == None:
        printError("<h1>404: Topic not found</h1>")
        return
    cursor.execute("SELECT name FROM categories WHERE id=?", (topicInfo[0],))
    catinfo = cursor.fetchone()
    username, admin = sessions.getSession(conn, cursor)
    print("Content-Type: text/html\n")
    buildHeader(username, admin)
    print("""<main><h1>%s</h1>
        <h3>Created by %s in category <a href="category.py?category=%d">%s</a></h3>""" % (topicInfo[2], topicInfo[1], topicInfo[0], catinfo[0]))
    if topicInfo[1] == username or admin:
        print("<a href='deleteTopic.py?topic=%s' class='delete'>Delete</a>" % (topicID,))
    print("""<p>%s</p>
        <h2>Comments</h2>
        <div class="elements">""" % (topicInfo[3],))

    for row in cursor.execute("SELECT commenter, comment, id FROM comments WHERE topicid=?", (topicID,)):
        print("<div class='element'><span>%s</span> <span><a href='user.py?user=%s'>%s</a>" % (row[1], quote(row[0]), row[0]))
        if row[0] == username or admin:
            print(" | <a href='deleteComment.py?commentid=%s' class='delete'>Delete</a>" % (row[2],))
        print("</span></div>")

    print("</div>")

    if username:
        print("""<div class='newcomment'>
        <h2>Write a Comment</h2>
        <form action='newComment.py' method='POST'>
            <input type='hidden' name='topicid' value='%d'>
            <label>
                Comment:<br/><textarea name='comment'></textarea>
            </label>
            <button>Comment</button>
        </form></div>""" % (topicID,))
    else:
        print("<h2>Log in to comment</h2>")
    print("""</main></body></html>""")

form = cgi.FieldStorage()
if "topic" not in form:
    print("Location: index.py\n")
else:
    try:
        main()
    except:
        print("Content-Type: text/html\n")
        raise
