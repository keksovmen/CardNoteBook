from tg.controllers.tgcontroller import TGController
from tg import request
from com.keksovmen.Util import *
from com.keksovmen.Model.ModelInit import ModelInit, updateInstance


class AbstractController(TGController):

	def create(self, **kwargs):
		form = self._getCreateForm(**kwargs)
		if self._isGetOrInvalid(form):
			return dict(form=form)
		obj = self._createModelObject(**kwargs)
		self._addToDb(obj)
		if "modelObject" not in kwargs.keys():
			kwargs["modelObject"] = obj
		self._actionAfterCreate(**kwargs)
		return dict(model=obj)

	def edit(self, **kwargs):
		pass

	def delete(self, **kwargs):
		pass

	def _checkRequestGet(self) -> bool:
		return request.method.lower() == "get"

	def _isGetOrInvalid(self, form: Form) -> bool:
		return self._checkRequestGet() or not form.isFormValid()

	def _addToDb(self, obj) -> None:
		ModelInit.session.add(obj)
		ModelInit.session.commit()

	def _getCreateForm(self, **kwargs) -> Form:
		pass

	def _createModelObject(self, **kwargs):
		pass

	def _actionAfterCreate(self, **kwargs):
		pass
