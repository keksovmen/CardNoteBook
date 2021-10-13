from tg import session, redirect
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import MovableController
from com.keksovmen.Decorators.Decorators import authenticated
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage, \
	isAcceptableLength, wrongLengthMessage
from com.keksovmen.Model.Card import Card
from com.keksovmen.Model.Constants import TEXT_SIZE, TITLE_SIZE, \
	DESCRIPTION_SIZE
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField


class CardController(MovableController):
	@expose()
	def index(self):
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/card/cardView.xhtml")
	@authenticated
	def view(self, card_id):
		return dict(card=Card.getCard(card_id, session.get('u_id', None)))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	@authenticated
	def create(self, dir_id: int = 0,
			   title=None,
			   description=None,
			   message=None,
			   **kwargs):
		result = super(CardController, self) \
			.create(dir_id=dir_id,
					title=title,
					description=description,
					message=message,
					user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		result['model'].updateModification()
		redirect("/dir/view?dir_id={}".format(dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	@authenticated
	def edit(self, card_id, title=None, description=None, message=None,
			 **kwargs):
		result = super(CardController, self) \
			.edit(card_id=card_id,
				  title=title,
				  description=description,
				  message=message,
				  user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		card = result['model']
		card.updateModification()
		redirect("/dir/view?dir_id={}".format(card.dir_id))

	@expose("com/keksovmen/Controllers/xhtml/card/card.xhtml")
	@authenticated
	def delete(self, card_id: int, **kwargs):
		result = super(CardController, self) \
			.delete(card_id=card_id,
					user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		redirect("/dir/view?dir_id={}".format(result['model'].dir_id))

	@expose("com/keksovmen/Controllers/xhtml/util/move.xhtml")
	@authenticated
	def move(self, card_id: int, parent_id=-1, **kwargs):
		result = super().move(parent_id,
							  card_id=card_id,
							  user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		redirect(f"/dir/view?dir_id={result['model'].dir_id}")

	def _getDefaultForm(self, **kwargs):
		form = Form()
		form.addField(
			FormField("title").addCheckCondition(
				checkNotZeroLength, zeroLengthMessage("Title"))
				.addCheckCondition(
				isAcceptableLength(TITLE_SIZE),
				wrongLengthMessage(TITLE_SIZE)))
		form.addField(FormField("card_id"))
		form.addField(FormField("description").addCheckCondition(
			isAcceptableLength(DESCRIPTION_SIZE),
			wrongLengthMessage(DESCRIPTION_SIZE)))
		form.addField(FormField("message").addCheckCondition(
			isAcceptableLength(TEXT_SIZE),
			wrongLengthMessage(TEXT_SIZE)))
		form.addField(FormField("pageTitle"))
		form.addField(FormField("button"))
		form.addField(FormField("action"))
		form.addField(FormField("dir_id"))
		form.setValues(**kwargs)
		return form

	def _getCreateForm(self, dir_id, title, description, message,
					   user_id) -> Form:
		form = self._getDefaultForm(dir_id=dir_id,
									title=title,
									description=description,
									message=message,
									pageTitle="Create card",
									button="Create",
									action="create")
		form.title.addCheckCondition(
			lambda v: Card.isNameFree(v, dir_id, user_id),
			"Such title already exists in current directory")
		return form

	def _getEditForm(self, model: Card,
					 card_id,
					 title,
					 description,
					 message,
					 **kwargs) -> Form:
		form = self._getDefaultForm(card_id=card_id,
									title=title,
									description=description,
									message=message,
									dir_id=model.dir_id,
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
									dir_id=card.dir_id,
									pageTitle="Delete card",
									button="Delete",
									action="delete")

	def _createModelObject(self, title, description, message, dir_id,
						   user_id) -> Card:
		return Card(title=title,
					description=description,
					message=message,
					dir_id=dir_id,
					card_id=User.generateCardId(user_id),
					creator=user_id)

	def _getModelObject(self, card_id, user_id, **kwargs) -> Card:
		return Card.getCard(card_id, user_id)

	def _updateFieldsOnGetEdit(self, model, kwargs: dict) -> None:
		kwargs['title'] = model.title
		kwargs['description'] = model.description
		kwargs['message'] = model.message

	def _updateMoveForm(self, form: Form, model: Card, parent_id):
		form.parent_id.addCheckCondition(
			lambda v: Card.isNameFree(
				model.title,
				parent_id,
				model.creator),
			"Such card name already exists in selected parent dir")
		form.current_dir.setValue(model.parent_dir)
		form.postfix.setValue(model.title)
		form.pageTitle.setValue("Move Card")
		form.view_style.setValue("card_holder")
		form.id_field.setValue("card_id")
