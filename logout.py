#!/usr/bin/python

import cgi
import cgitb
import sqlite3
cgitb.enable()
import sessions

def main():
    conn = sqlite3.connect("../www/forum.db")
    cursor = conn.cursor()
    sessions.deleteSession(conn, cursor)
    # turns out the spec-compliant way of deleting a cookie is setting it to expire in the past
    print("Set-Cookie: sid=farts; expires=Thu, 01 Jan 1970 00:00:00 GMT")
    print("Location: index.py\n")
try: 
    main()
except Exception as ex:
    print("Content-type: text/html\n")
    raise
