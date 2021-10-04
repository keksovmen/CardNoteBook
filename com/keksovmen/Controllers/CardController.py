from tg import session, redirect
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import AbstractController
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage
from com.keksovmen.Model.Directory import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField


class CardController(AbstractController):
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
		result = super(CardController, self).create(dir_id=dir_id,
													title=title,
													description=description,
													message=message)
		if "form" in result.keys():
			return result
		result['model'].updateModification()
		redirect("/dir/view?dir_id={}".format(dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	def edit(self, card_id, title=None, description=None, message=None):
		result = super(CardController, self).edit(card_id=card_id,
												  title=title,
												  description=description,
												  message=message)
		if "form" in result.keys():
			return result
		card = result['model']
		card.updateModification()
		redirect("/dir/view?dir_id={}".format(card.dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	def delete(self, card_id: int):
		result = super(CardController, self).delete(card_id=card_id)
		if "form" in result.keys():
			return result
		redirect("/dir/view?dir_id={}".format(result['model'].dir_id))

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

	def _getEditForm(self, model: Card,
					 card_id,
					 title,
					 description,
					 message) -> Form:
		form = self._getDefaultForm(card_id=card_id,
									title=title,
									description=description,
									message=message,
									pageTitle="Edit card",
									button="Save",
									action="edit")
		form.title.addCheckCondition(
			lambda v: model.isEditTitleFree(title),
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

	def _createModelObject(self, title, description, message, dir_id) -> Card:
		return Card(title=title,
					description=description,
					message=message,
					dir_id=dir_id,
					card_id=User.generateCardId(session['u_id']),
					creator=session['u_id'])

	def _getModelObject(self, card_id, **kwargs) -> Card:
		return Card.getCard(card_id, session['u_id'])

	def _updateFieldsOnGetEdit(self, model, kwargs: dict) -> None:
		kwargs['title'] = model.title
		kwargs['description'] = model.description
		kwargs['message'] = model.message
