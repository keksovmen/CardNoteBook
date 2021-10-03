import sqlalchemy
from tg import session, redirect, request
from tg.controllers.tgcontroller import TGController
from tg.decorators import expose

from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.ModelInit import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import *
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage


class UserController(TGController):

	@expose()
	def index(self):
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def login(self, name=None, password=None):
		form = self._getLoginForm(name, password)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		me = ModelInit.session.query(User).filter(User.name == name).first()
		self._saveUserInSession(me)
		redirect()

	@expose()
	def logout(self):
		session.delete()
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def create(self, name=None, password=None):
		form = self._getCreateForm(name, password)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		me = User(name=name, password=password)
		me.dirs.append(Directory(title="root", dir_id=0, parent_id=None))
		ModelInit.session.add(me)
		ModelInit.session.commit()
		self._saveUserInSession(me)
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def edit(self, name=None, password=None):
		me = User.getMe(session)
		if request.method.lower() == "get":
			name = me.name
			password = me.password
		form = self._getEditForm(name, password, me)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		updateInstance(me, name=name, password=password)
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def delete(self):
		form = self._getDeleteForm()
		if request.method.lower() == "get":
			return dict(form=form)
		me = User.getMe(session)
		ModelInit.session.delete(me)
		ModelInit.session.commit()
		session.delete()
		redirect()

	def _saveUserInSession(self, user: User):
		session['u_id'] = user.u_id
		session['name'] = user.name
		session.save()

	def _getDefaultForm(self, **kwargs):
		form = Form()
		form.addField(
			FormField("name").addCheckCondition(
				checkNotZeroLength,
				zeroLengthMessage("Name")))
		form.addField(
			FormField("password").addCheckCondition(
				checkNotZeroLength,
				zeroLengthMessage("Password")))

		form.addField(FormField("pageTitle"))
		form.addField(FormField("button"))
		form.addField(FormField("action"))

		form.setValues(**kwargs)
		return form

	def _getLoginForm(self, name, password):
		form = self._getDefaultForm(name=name,
									password=password,
									pageTitle="Login",
									button="Login",
									action="login")
		form.name.addCheckCondition(
			lambda v: ModelInit.session.query(User) \
						  .filter(User.name == v) \
						  .filter(User.password == password).count() != 0,
			"Wrong login or password")
		return form

	def _getCreateForm(self, name, password):
		form = self._getDefaultForm(name=name,
									password=password,
									pageTitle="Registration",
									button="Register",
									action="create")
		form.name.addCheckCondition(
			lambda v: User.isNameFree(v),
			"Such name already exists")
		return form

	def _getEditForm(self, name, password, user: User):
		form = self._getDefaultForm(name=name,
									password=password,
									pageTitle="Edit profile",
									button="Save",
									action="edit")
		form.name.addCheckCondition(
			lambda v: user.isEditNameFree(v),
			"Such name already exists")
		return form

	def _getDeleteForm(self):
		return self._getDefaultForm(pageTitle="Account deletion",
									button="Delete",
									action="delete")
