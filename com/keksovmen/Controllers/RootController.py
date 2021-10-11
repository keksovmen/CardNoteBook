from tg import redirect
from tg.controllers.tgcontroller import TGController
from tg.decorators import expose

from com.keksovmen.Controllers.CardController import CardController
from com.keksovmen.Controllers.DirectoryController import DirectoryController
from com.keksovmen.Controllers.UserController import UserController


class RootController(TGController):
	user = UserController()
	dir = DirectoryController()
	card = CardController()

	@expose()
	def index(self):
		redirect("/dir/view")




