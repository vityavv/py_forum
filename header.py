def buildHeader(username, admin):
    print("""<!DOCTYPE html>
    <html>
    <head>
        <title>Victor's Forum</title>
        <link rel="stylesheet" type="text/css" href="nord.css"/>
        <link rel="stylesheet" type="text/css" href="css.css"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="UTF-8">
    </head>
    <body>""")

    print("<header><span><b><a href='index.py'>Victor's Forum</a></b> | <a href='about.py'>About</a></span> <span>")
    if username:
        if admin:
            print("Logged in as " + username + " <b>(admin)</b> <a href='admin.py'>Admin Dashboard</a> <a href='logout.py' class='button'>Log out</a>")
        else:
            print("Logged in as " + username + " <a href='logout.py' class='button'>Log out</a>")
    else:
        print("""<form action='login.py' method='POST'>
            <label>Username: <input name='username' type='text'/></label>
            <label>Password: <input name='password' type='password'/></label>
            <button type='submit'>Log In</button>
        </form><a href="login.html" class="button" id="smallscreenproblems">Log In</a> <a href='newUser.html' class="button">New User</a>""")
    print("</span></header>")
