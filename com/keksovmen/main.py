from wsgiref.simple_server import make_server

from com.keksovmen.Configurators.Configurator import Configurator
from com.keksovmen.Controllers.RootController import RootController
from com.keksovmen.Model.ModelInit import ModelInit

configurator = Configurator()
configurator.setRootController(RootController())
configurator.enableSql("sqlite:///database.db", ModelInit.session, ModelInit.init_model)
configurator.enableSessions("cache/sessions/")
configurator.enableStatic("public/")
application = configurator.getConfig().make_wsgi_app()
httpd = make_server("localhost", 8080, application)
httpd.serve_forever()
