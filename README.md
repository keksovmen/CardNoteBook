# CardNoteBook
WSGI app, based on TurboGears2 framework on minimalApplicationConfiguration with additional components<br/>

You could connect it to Appache web server (check TurboGears site for how to)<br/>
or you can use it as stend alone application for yourself, because for "prodaction"<br/>
you will need to change WSGI server from BaseHTTP, due to HTTP 2.+ there is connection: keep-alive<br/>
and on my settings (Opera) single socket connection is holded by browser until it dies ~1-2 min<br/>
<hr/>
<h2>What not implemented, and probably won't be:</h2><br/>
Proper authenication through TurboGears, now it is just session, with redirects to login/register form<br/>
Rebasing on fullStackApplicationConfiguration<br/>
Javascript for maybe ajax calls<br/>
Probbably something else but i can't recall<br/>
<hr/>
<h2>What was interesting:</h2><br/>
Password storage as salt and salted hash<br/>
SQL - self linking list with foreign keys as part of primary<br/>
SQL - ORM through SQLAlchemy, upper part didn't want to work without specifiend primaryjoin<br/>
Basic html/css<br/>
