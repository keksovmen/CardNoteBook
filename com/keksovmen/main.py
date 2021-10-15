import sys
import webbrowser

import tg

from com.keksovmen.Util import Globals

args = sys.argv[1:]
try:
	g = Globals.createFromCommandLine(args)
except:
	print(Globals.allowedArguments())
	raise

# for underlying imports to initialise function default arguments
tg.app_globals = g

from wsgiref.simple_server import make_server
from threading import Thread

from com.keksovmen.Configurators.Configurator import Configurator
from com.keksovmen.Controllers.RootController import RootController
from com.keksovmen.Model.ModelInit import ModelInit


def httpLoop():
	global httpd
	httpd.serve_forever(1)


def inputLoop():
	while True:
		cmd = input()
		if cmd == "q":
			global httpd
			# you can just return from the loop,
			# due to httpLoop is Deamon process will terminate
			httpd.socket.close()
			# won't work as expected, due to connection: keep-alive of http 2
			# at lest in desktop opera, you will have to wait around a minute
			# for the connection to die
			# httpd.shutdown()
			# ugly but works without calling windows error handler
			sys.exit()
		if cmd == "o":
			webbrowser.open("http://localhost:8080")


configurator = Configurator(args)
configurator.setRootController(RootController())
configurator.enableSql(f"sqlite:///{g.database}",
					   ModelInit.session,
					   ModelInit.init_model)
configurator.enableSessions(g.sessionCache)
configurator.enableStatic("public/")
application = configurator.getConfig().make_wsgi_app()
httpd = make_server("localhost", g.port, application)

print("Possible commands:\n",
	  "\tq - for closing the app\n",
	  "\to - for opening web bworser with app tab")

Thread(target=httpLoop, daemon=True).start()
Thread(target=inputLoop, daemon=False).start()
