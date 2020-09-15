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
    if "category" not in form:
        printError("Category not given")

    categoryIDs = form["category"].value
    if not categoryIDs.isdigit():
        printError("Category ID must be digit")
        return
    categoryID = int(categoryIDs)
    # Not needed bc query won't fail if not deleting anything
    #cursor.execute("SELECT * FROM categories WHERE id=?", (categoryID,))
    #if cursor.fetchone() == None:
        #printError("Category with that ID not found")
        #return

    _, admin = sessions.getSession(conn, cursor)
    if not admin:
        printError("You're not logged into an admin account, so you can't delete a category")

    cursor.execute("DELETE FROM categories WHERE id=?", (categoryID,))
    #cursor.execute("DELETE comments FROM comments INNER JOIN topics ON comments.topicid=topics.id WHERE topics.categoryid=?", (categoryID,))
    cursor.execute("DELETE FROM comments WHERE comments.topicid IN (SELECT id FROM topics WHERE categoryid=?)", (categoryID,))
    cursor.execute("DELETE FROM topics WHERE categoryid=?", (categoryID,))

    conn.commit()

    print("Location: admin.py\n")
    conn.close()
    
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
