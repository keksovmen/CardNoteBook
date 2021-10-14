import sys

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

from com.keksovmen.Configurators.Configurator import Configurator
from com.keksovmen.Controllers.RootController import RootController
from com.keksovmen.Model.ModelInit import ModelInit

configurator = Configurator(args)
configurator.setRootController(RootController())
configurator.enableSql(f"sqlite:///{g.database}",
					   ModelInit.session,
					   ModelInit.init_model)
configurator.enableSessions(g.sessionCache)
configurator.enableStatic("public/")
application = configurator.getConfig().make_wsgi_app()
httpd = make_server("localhost", g.port, application)
httpd.serve_forever()
