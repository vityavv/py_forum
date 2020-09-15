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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topics'")
    if cursor.fetchone() == None:
        initDB.initDB(cursor)
        conn.commit()

    categoryIDs = form["category"].value
    if not categoryIDs.isdigit():
        printError("Category ID must be number")
        return
    categoryID = int(categoryIDs)
    cursor.execute("SELECT name, desc FROM categories WHERE id=?", (categoryID,))
    catinfo = cursor.fetchone()
    if catinfo == None:
        printError("<h1>404: Category not found</h1>")
        return
    username, admin = sessions.getSession(conn, cursor)
    print("Content-Type: text/html\n")
    buildHeader(username, admin)
    print("""<main><h1>Topics in category "%s"</h1>
        <p>Category Description: %s</p><div class="elements">""" % catinfo)

    for row in cursor.execute("SELECT creator, name, id FROM topics WHERE categoryid=?", (categoryID,)):
        print("<div class='element'><a href='topic.py?topic=%s'>%s</a> <span>(Created by <a href='user.py?user=%s'>%s</a>)" % (row[2], row[1], quote(row[0]), row[0]))
        if admin or username == row[0]:
            print(" <a href='deleteTopic.py?topic=%s' class='delete'>Delete</a>" % (row[2],))
        print("</span></div>")

    print("</div>")
    if username:
        print("""<div class='newtopic'>
        <h2>New topic in this Category</h2>
        <form action='newTopic.py' method='POST'>
            <input type='hidden' name='categoryid' value='%d'/>
            <label>
                Topic name: <input type='text' name='topicname'/>
            </label><br/>
            <label>
                Topic body:<br/> <textarea name='topicbody'></textarea>
            </label><br/>
            <button type='submit'>Create Topic</button>
        </form></div>""" % categoryID)
    else:
        print("<h2>Log in to create a topic</h2>")


    print("""</main></body></html>""")

form = cgi.FieldStorage()
if "category" not in form:
    print("Location: index.py\n")
else:
    try:
        main()
    except:
        print("Content-Type: text/html\n")
        raise
