#!/usr/bin/python3

import sqlite3
import sessions
import cgitb
cgitb.enable()
from header import buildHeader

print("Content-Type: text/html\n")
conn = sqlite3.connect("../www/forum.db")
cursor = conn.cursor()
username, admin = sessions.getSession(conn, cursor)
buildHeader(username, admin)
print("""<body>
        <main>
            <h1>About this site</h1>
            <p>This project, named "Victor's Forum," is a forum created by me, Victor Veytsman. On it, users can interact by creating posts (called "topics") in different categories, and then reply to each-others' posts. Credits go to <a href="https://www.nordtheme.com/">Nord Theme</a> for providing the color scheme and to sites such as the Mozilla Developer Network and StackOverflow for documentation and helping me fix bugs.</p>
            <h2>Usage Video</h2>
            <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/em4QloxQGWw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <h2>Reflection</h2>
            <p>Creating this project has been very fun. I set a constraint for myself to not use JavaScript, because I'm already really comfortable with it and I wanted to see how far I could go with just HTML, CSS, and Python. I had fun creating the sessions system from scratch---before I had only ever used 3rd party sessions libraries in my projects. It was also fun to make the site mobile-compatible, as without JavaScript I had to figure out a way to change some of the content in the header based on the screen size while still making it usable. Overall, this has been a lot of fun.</p>
            <h2>Credits</h2>
            <p>Thanks to Isabelle Lam for pointing out errors in my site and helping me out, as well as testing the site when I finished. Thanks to Jasmine Wang for pasting the entire bee movie script into a post and helping me find a CSS bug. Thanks to Kim Justin for breaking the site and forcing me to add unicode support. Thanks to Stephanie Liu, Brandonn Guzman, and Kim Justin for putting HTML into their posts and their usernames, forcing me to find and fix the bug that wouldn't escape said HTML.</p>
        </main></body></html>""")
