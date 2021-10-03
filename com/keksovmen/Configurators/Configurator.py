from tg.configurator.minimal import MinimalApplicationConfigurator
from tg.configurator.components.statics import StaticsConfigurationComponent

config = MinimalApplicationConfigurator()
config.update_blueprint({
	"server_static": True,
	"paths": {
		"static_files": "public"
	}
})

config.update_blueprint({
	"server_static": True,
	"paths": {
		"static_files": "public"
	}
})

config.register(StaticsConfigurationComponent)

