import uuid
import os
import html

def _getcookies():
    return dict(map(lambda s: s.split("="), os.environ["HTTP_COOKIE"].split(";")))

def newSession(conn, cursor, username, admin):
    cursor.execute("CREATE TABLE IF NOT EXISTS sessions (sessionid STRING PRIMARY KEY, username STRING, admin BOOLEAN, age INTEGER)")
    sessionID = uuid.uuid4()
    # true if.. part is bc admin is stored as an int but sqlite expects it to be a bool smh
    cursor.execute("INSERT INTO sessions (sessionid, username, admin, age) VALUES (?, ?, ?, datetime('now'))", (str(sessionID), html.escape(html.unescape(username)), True if admin else False))
    conn.commit()
    return str(sessionID)

def getSession(conn, cursor): #returns (username, admin?)
    if "HTTP_COOKIE" not in os.environ.keys():
        return (None, None)
    session = _getcookies()
    if "sid" not in session:
        return (None, None)
    sessionID = session["sid"]
    cursor.execute("CREATE TABLE IF NOT EXISTS sessions (sessionid STRING PRIMARY KEY, username STRING, admin BOOLEAN, age INTEGER)")
    conn.commit()
    cursor.execute("SELECT username, admin FROM sessions WHERE sessionid=?", (sessionID,))
    result = cursor.fetchone()
    if result == None:
        return (None, None)
    return result

def deleteSession(conn, cursor):
    if "HTTP_COOKIE" not in os.environ.keys():
        return
    session = _getcookies()
    if "sid" not in session:
        return (None, None)
    sessionID = session["sid"]
    cursor.execute("DELETE FROM sessions WHERE sessionid=?", (sessionID,))
    conn.commit()
