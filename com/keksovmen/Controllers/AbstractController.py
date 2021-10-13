from tg import request
from tg.controllers.tgcontroller import TGController

from com.keksovmen.Model.ModelInit import ModelInit, updateInstance
from com.keksovmen.Util import *

__all__ = ["AbstractController", "MovableController"]


class AbstractController(TGController):

	def create(self, **kwargs) -> dict:
		form = self._getCreateForm(**kwargs)
		if self._isGetOrInvalid(form):
			return dict(form=form)
		model = self._createModelObject(**kwargs)
		self._addToDb(model)
		return dict(model=model)

	def edit(self, **kwargs) -> dict:
		model = self._getModelObject(**kwargs)
		if self._isRequestGet():
			self._updateFieldsOnGetEdit(model, kwargs)
		form = self._getEditForm(model, **kwargs)
		if self._isGetOrInvalid(form):
			return dict(form=form)
		self._updateInstance(model, **kwargs)
		return dict(model=model)

	def delete(self, **kwargs) -> dict:
		model = self._getModelObject(**kwargs)
		form = self._getDeleteForm(model)
		if self._isGetOrInvalid(form):
			return dict(form=form)
		self._deleteModelObject(model)
		return dict(model=model)

	def _isRequestGet(self) -> bool:
		return request.method.lower() == "get"

	def _isGetOrInvalid(self, form: Form) -> bool:
		return self._isRequestGet() or not form.isFormValid()

	def _addToDb(self, obj) -> None:
		ModelInit.session.add(obj)
		ModelInit.session.commit()

	def _updateInstance(self, model, **kwargs):
		updateInstance(model, **kwargs)

	def _deleteModelObject(self, model):
		ModelInit.session.delete(model)
		ModelInit.session.commit()

	def _getCreateForm(self, **kwargs) -> Form:
		pass

	def _createModelObject(self, **kwargs) -> object:
		pass

	def _getModelObject(self, **kwargs) -> object:
		pass

	def _updateFieldsOnGetEdit(self, model, kwargs: dict) -> None:
		pass

	def _getEditForm(self, model, **kwargs) -> Form:
		pass

	def _getDeleteForm(self, model) -> Form:
		pass


class MovableController(AbstractController):
	def move(self, parent_id=-1, **kwargs):
		model = self._getModelObject(**kwargs)
		if parent_id == -1:
			parent_id = model.getParentId()
		form = self.__getMoveForm(model,
								  parent_id,
								  model.getPossibleParents())
		self._updateMoveForm(form, model, parent_id)
		if self._isGetOrInvalid(form):
			return dict(form=form)
		model.move(parent_id)
		return dict(model=model)

	def _updateMoveForm(self, form: Form, model, parent_id):
		pass

	def __getMoveForm(self, model, parent_id, possible_parents):
		form = Form()
		form.addField(FormField("current_id", model.getId()))
		form.addField(FormField("parent_id", parent_id)
			.addCheckCondition(
			lambda v: v != -1,
			"You didn't select any parent directory"))
		form.addField(FormField("possible_parents", possible_parents))
		form.addField(FormField("back_link", f"/dir/view?dir_id={parent_id}"))
		# Don't forget to update them especially current_dir
		form.addField(FormField("current_dir"))
		form.addField(FormField("postfix", ""))
		form.addField(FormField("pageTitle"))
		form.addField(FormField("view_style"))
		form.addField(FormField("id_field"))
		return form
