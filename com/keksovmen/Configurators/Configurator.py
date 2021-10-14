from tg import ApplicationConfigurator
from tg.configurator.components.session import SessionConfigurationComponent
from tg.configurator.components.sqlalchemy import \
	SQLAlchemyConfigurationComponent
from tg.configurator.components.statics import StaticsConfigurationComponent
from tg.configurator.minimal import MinimalApplicationConfigurator
from tg.util.bunch import Bunch

from com.keksovmen.Helpers import Helpers
from com.keksovmen.Util import Globals


class Configurator:
	_config: ApplicationConfigurator

	def __init__(self, arguments: list):
		self._config = MinimalApplicationConfigurator()
		self._config.update_blueprint({
			"app_globals": Globals.functionCreateFromCommandLine(arguments)
		})

	def setRootController(self, controller):
		self._config.update_blueprint({
			"root_controller": controller,
			"renderers": ["kajiki"],
			"helpers": Helpers
		})

	def enableStatic(self, path: str):
		self._config.register(StaticsConfigurationComponent)
		self._config.update_blueprint({
			"serve_static": True,
			"paths": {
				"static_files": path
			}
		})

	def enableSessions(self, path: str):
		self._config.register(SessionConfigurationComponent)
		self._config.update_blueprint({
			"session.enabled": True,
			"session.data_dir": path
		})

	def enableSql(self, url: str, session, initFunction):
		self._config.register(SQLAlchemyConfigurationComponent)
		self._config.update_blueprint({
			"use_sqlalchemy": True,
			"sqlalchemy.url": url,
			"model": Bunch(
				DBSession=session,
				init_model=initFunction
			)
		})

	def getConfig(self) -> ApplicationConfigurator:
		return self._config
