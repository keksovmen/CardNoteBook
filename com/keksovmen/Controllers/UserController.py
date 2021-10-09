from tg import session, redirect, request
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import AbstractController
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage
from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.ModelInit import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import *
from com.keksovmen.Decorators.Authenticator import authenticated


class UserController(AbstractController):

	@expose("com/keksovmen/Controllers/xhtml/user/userGuide.xhtml")
	def index(self):
		return dict()

	@expose("com/keksovmen/Controllers/xhtml/user/userView.xhtml")
	@authenticated
	def view(self, **kwargs):
		me = User.getMe(session.get('u_id', None))
		return dict(user=me)

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def login(self, name=None, password=None, **kwargs):
		form = self._getLoginForm(name, password)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		me = ModelInit.session.query(User).filter(User.name == name).first()
		self._saveUserInSession(me)
		redirect()

	@expose()
	def logout(self, **kwargs):
		session.delete()
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	def create(self, name=None, password=None, **kwargs):
		result = super(UserController, self).create(name=name,
													password=password)
		if "form" in result.keys():
			return result
		self._saveUserInSession(result['model'])
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	@authenticated
	def edit(self, name=None, password=None, **kwargs):
		result = super(UserController, self).edit(name=name,
												  password=password)
		if "form" in result.keys():
			return result
		self._saveUserInSession(result['model'])
		redirect()

	@expose("com/keksovmen/Controllers/xhtml/user/user.xhtml")
	@authenticated
	def delete(self, **kwargs):
		result = super(UserController, self).delete()
		if "form" in result.keys():
			return result
		session.delete()
		redirect()

	def _saveUserInSession(self, user: User):
		session['u_id'] = user.u_id
		session['u_name'] = user.name
		session.save()

	def _getDefaultForm(self, **kwargs) -> Form:
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

	def _getLoginForm(self, name, password) -> Form:
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

	def _getCreateForm(self, name, password) -> Form:
		form = self._getDefaultForm(name=name,
									password=password,
									pageTitle="Registration",
									button="Register",
									action="create")
		form.name.addCheckCondition(
			lambda v: User.isNameFree(v),
			"Such name already exists")
		return form

	def _getEditForm(self, user: User, name, password) -> Form:
		form = self._getDefaultForm(name=name,
									password=password,
									pageTitle="Edit profile",
									button="Save",
									action="edit")
		form.name.addCheckCondition(
			lambda v: user.isEditNameFree(v),
			"Such name already exists")
		return form

	def _getDeleteForm(self, model: User) -> Form:
		form = self._getDefaultForm(pageTitle="Account deletion",
									button="Delete",
									action="delete")
		form.clearAllValidationChecks()
		return form

	def _createModelObject(self, name, password) -> User:
		me = User(name=name, password=password)
		me.dirs.append(Directory(title="root", dir_id=0, parent_id=None))
		return me

	def _getModelObject(self, **kwargs) -> User:
		return User.getMe(session.get('u_id', None))

	def _updateFieldsOnGetEdit(self, model: User, kwargs: dict) -> None:
		kwargs['name'] = model.name
		kwargs['password'] = model.password
