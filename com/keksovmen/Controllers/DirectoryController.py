from tg import session, redirect
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import AbstractController
from com.keksovmen.Decorators.Authenticator import authenticated
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage, \
	PaginatorHandler
from com.keksovmen.Model.Directory import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField


class DirectoryController(AbstractController):

	@expose()
	def index(self):
		redirect("/dir/view")

	@expose("com/keksovmen/Controllers/xhtml/dir/directoryView.xhtml")
	@authenticated
	def view(self, dir_id: int = 0, page: int = 0, step: int = 3):
		current_dir = ModelInit.session.query(Directory) \
			.filter(Directory.creator == session.get('u_id', None)) \
			.filter(Directory.dir_id == dir_id).first()
		paginator = PaginatorHandler(max(len(current_dir.children),
										 len(current_dir.cards)),
									 int(page),
									 int(step),
									 10)
		return dict(current_dir=current_dir, paginator=paginator)

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	@authenticated
	def create(self, parent_id: int, title=None, description=None, **kwargs):
		result = super(DirectoryController, self).create(
			parent_id=int(parent_id),
			title=title,
			description=description,
			user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		currDir = result["model"]
		currDir.updateModification()
		redirect("view?dir_id={}".format(currDir.dir_id))

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	@authenticated
	def edit(self, dir_id: int, title=None, description=None, **kwargs):
		result = super(DirectoryController, self).edit(
			dir_id=dir_id,
			title=title,
			description=description,
			user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		currDir = result["model"]
		currDir.updateModification()
		redirect("view?dir_id={}".format(
			currDir.parent.dir_id if currDir.parent else 0))

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	@authenticated
	def delete(self, dir_id: int, **kwargs):
		result = super(DirectoryController, self) \
			.delete(dir_id=dir_id, user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		currDir = result["model"]
		redirect("view?dir_id={}".format(currDir.parent_id))

	def _getDefaultForm(self, **kwargs):
		form = Form()
		form.addField(
			FormField("title").addCheckCondition(
				checkNotZeroLength, zeroLengthMessage("Title")))
		form.addField(FormField("description"))
		form.addField(FormField("dir_id"))
		form.addField(FormField("parent_id"))
		form.addField(FormField("pageTitle"))
		form.addField(FormField("button"))
		form.addField(FormField("action"))
		form.addField(FormField("action"))
		form.setValues(**kwargs)
		return form

	def _getCreateForm(self, parent_id, title, description, user_id) -> Form:
		form = self._getDefaultForm(title=title,
									description=description,
									parent_id=parent_id,
									pageTitle="Create directory",
									action="create",
									button="Create")
		form.title.addCheckCondition(
			lambda v: Directory.isNameFree(title, parent_id, user_id),
			"Such title already exists in current directory")
		return form

	def _getEditForm(self, model: Directory,
					 title,
					 description,
					 dir_id,
					 **kwargs) -> Form:
		form = self._getDefaultForm(title=title,
									description=description,
									dir_id=dir_id,
									parent_id=model.parent_id,
									pageTitle="Edit directory",
									action="edit",
									button="Save")
		form.title.addCheckCondition(
			lambda v: model.isEditTitleFree(title),
			"Such title already exists in current directory")
		return form

	def _getDeleteForm(self, directory: Directory) -> Form:
		form = self._getDefaultForm(title=directory.title,
									description=directory.description,
									dir_id=directory.dir_id,
									parent_id=directory.parent_id,
									pageTitle="Delete directory",
									action="delete",
									button="Delete")
		form.addField(FormField("dir", directory))
		return form

	def _createModelObject(self, parent_id, title, description, user_id):
		return Directory(title=title,
						 description=description,
						 creator=user_id,
						 dir_id=User.generateDirectoryId(user_id),
						 parent_id=parent_id)

	def _getModelObject(self, dir_id, user_id, **kwargs) -> Directory:
		return Directory.getDirectory(dir_id, user_id)

	def _updateFieldsOnGetEdit(self, model: Directory, kwargs: dict):
		kwargs['title'] = model.title
		kwargs['description'] = model.description
