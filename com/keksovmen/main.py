import sys
from wsgiref.simple_server import make_server

from com.keksovmen.Configurators.Configurator import Configurator
from com.keksovmen.Controllers.RootController import RootController
from com.keksovmen.Model.ModelInit import ModelInit

try:
	port = int(sys.argv[1])
except IndexError:
	port = 8080

try:
	database = sys.argv[2]
except IndexError:
	database = "database.db"

configurator = Configurator()
configurator.setRootController(RootController())
configurator.enableSql(f"sqlite:///{database}", ModelInit.session, ModelInit.init_model)
configurator.enableSessions("cache/sessions/")
configurator.enableStatic("public/")
application = configurator.getConfig().make_wsgi_app()
httpd = make_server("localhost", port, application)
httpd.serve_forever()
