from tg import request, redirect, session
from tg.controllers.tgcontroller import TGController
from tg.decorators import expose

from com.keksovmen.Controllers.UserController import UserController
from com.keksovmen.Controllers.DirectoryController import DirectoryController
from com.keksovmen.Controllers.CardController import CardController
from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.ModelInit import ModelInit
from com.keksovmen.Model.User import User
from com.keksovmen.Util import *


class RootController(TGController):
	user = UserController()
	dir = DirectoryController()
	card = CardController()

	@expose()
	def index(self):
		redirect("/dir/view")




