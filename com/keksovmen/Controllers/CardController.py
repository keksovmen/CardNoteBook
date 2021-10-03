import sqlalchemy
import inspect
from tg import session, redirect, request
from tg.controllers.tgcontroller import TGController
from tg.decorators import expose

from com.keksovmen.Model.ModelInit import *
from com.keksovmen.Model.Directory import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage


class CardController(TGController):
	@expose()
	def index(self):
		pass

	@expose("com/keksovmen/Controllers/xhtml/card/cardView.xhtml")
	def view(self, card_id):
		return dict(card=Card.getCard(card_id, session['u_id']))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	def create(self, dir_id: int = 0,
			   title=None,
			   description=None,
			   message=None):
		form = self._getCreateForm(dir_id, title, description, message)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)

		card = Card(title=title,
					description=description,
					message=message,
					dir_id=dir_id,
					card_id=User.generateCardId(session['u_id']),
					creator=session['u_id'])
		ModelInit.session.add(card)
		ModelInit.session.commit()
		card.updateModification()
		redirect("/dir/view?dir_id={}".format(dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	def edit(self, card_id, title=None, description=None, message=None):
		card = Card.getCard(card_id, session['u_id'])
		if request.method.lower() == "get":
			title = card.title
			description = card.description
			message = card.message

		form = self._getEditForm(title, description, message, card)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		updateInstance(card,
					   title=title,
					   description=description,
					   message=message)
		redirect("/dir/view?dir_id={}".format(card.dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	def delete(self, card_id: int):
		card = Card.getCard(card_id, session['u_id'])
		form = self._getDeleteForm(card)
		if request.method.lower() == "get":
			return dict(form=form)
		ModelInit.session.delete(card)
		ModelInit.session.commit()
		redirect("/dir/view?dir_id={}".format(card.dir_id))

	def _getDefaultForm(self, **kwargs):
		form = Form()
		form.addField(
			FormField("title").addCheckCondition(
				checkNotZeroLength, zeroLengthMessage("Title")))
		form.addField(FormField("card_id"))
		form.addField(FormField("description"))
		form.addField(FormField("message"))
		form.addField(FormField("pageTitle"))
		form.addField(FormField("button"))
		form.addField(FormField("action"))
		form.addField(FormField("dir_id"))
		form.setValues(**kwargs)
		return form

	def _getCreateForm(self, dir_id, title, description, message) -> Form:
		form = self._getDefaultForm(dir_id=dir_id,
									title=title,
									description=description,
									message=message,
									pageTitle="Create card",
									button="Create",
									action="create")
		form.title.addCheckCondition(
			lambda v: Card.isNameFree(v, dir_id, session['u_id']),
			"Such title already exists in current directory")
		return form

	def _getEditForm(self, title, description, message, card: Card) -> Form:
		form = self._getDefaultForm(card_id=card.card_id,
									title=title,
									description=description,
									message=message,
									pageTitle="Edit card",
									button="Save",
									action="edit")
		form.title.addCheckCondition(
			lambda v: card.isEditTitleFree(title),
			"Such title already exists in current directory")
		return form

	def _getDeleteForm(self, card: Card) -> Form:
		return self._getDefaultForm(title=card.title,
									card_id=card.card_id,
									description=card.description,
									message=card.message,
									pageTitle="Delete card",
									button="Delete",
									action="delete")
