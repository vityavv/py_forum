#!/usr/bin/python

import cgi
import cgitb
import sqlite3
import crypt
import html
cgitb.enable()

def printError(err):
    print("Content-type: text/html\n")
    print("<h1>" + err + "</h1>")

def main():
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username STRING PRIMARY KEY, password STRING, admin BOOLEAN)")

    form = cgi.FieldStorage()
    if "username" not in form or "password" not in form:
        printError("Missing form values")
        return

    try: 
        cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (html.escape(html.unescape(form["username"].value)), crypt.crypt(form["password"].value), form["username"].value == "victor"))
        conn.commit()
        conn.close()
    except sqlite3.Error as ex:
        printError(str(ex))
        return
    
    #print("Location:index.html\n")
    print("Content-type: text/html\n")
    print("""<!DOCTYPE html>
<html>
    <head><title>User Created Successfully</title></head>
    <body><h1>User Created Successfully</h1><a href="index.py">Home</a></body>
</html>""")

try: 
    main()
except Exception as ex:
    printError(str(ex))
