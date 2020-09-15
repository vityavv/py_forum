#!/usr/bin/python

import cgi
import cgitb
import sqlite3
import crypt
cgitb.enable()
import sessions
import html
from hmac import compare_digest as compare_hash

def printError(err):
    print("Content-type: text/html\n")
    print("<h1>" + err + "</h1>")

def main():
    form = cgi.FieldStorage()
    requiredFields = ["username", "password"]
    for field in requiredFields:
        if field not in form:
            printError("Missing form value: " + field)
            return
    
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password, admin FROM users WHERE username=?", (html.escape(html.unescape(form["username"].value)),))
    row = cursor.fetchone()
    if row == None:
        printError("User not found")
        return
    if not compare_hash(crypt.crypt(form["password"].value, row[0]), row[0]):
        printError("Incorrect password")
        return
    
    sessionID = sessions.newSession(conn, cursor, form["username"].value, row[1])
    print("Set-Cookie: sid=" + sessionID)
    print("Location: index.py")
    print()

try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
