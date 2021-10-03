from tg.controllers.tgcontroller import TGController
from tg import request
from com.keksovmen.Util import *
from com.keksovmen.Model.ModelInit import ModelInit, updateInstance


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
		pass

	def delete(self, **kwargs) -> dict:
		pass

	def _isRequestGet(self) -> bool:
		return request.method.lower() == "get"

	def _isGetOrInvalid(self, form: Form) -> bool:
		return self._isRequestGet() or not form.isFormValid()

	def _addToDb(self, obj) -> None:
		ModelInit.session.add(obj)
		ModelInit.session.commit()

	def _updateInstance(self, model, **kwargs):
		updateInstance(model, **kwargs)

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
