from tg import session, redirect
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import MovableController
from com.keksovmen.Decorators.Authenticator import authenticated
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage, \
	isAcceptableLength, wrongLengthMessage
from com.keksovmen.Helpers.Paginator import PaginatorHandler
from com.keksovmen.Model.Constants import TITLE_SIZE, DESCRIPTION_SIZE
from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField


class DirectoryController(MovableController):

	@expose()
	def index(self):
		redirect("/dir/view")

	@expose("com/keksovmen/Controllers/xhtml/dir/directoryView.xhtml")
	@authenticated
	def view(self, dir_id: int = 0, page: int = 0, step: int = 3):
		current_dir = Directory.getDirectory(dir_id, session.get('u_id', None))
		paginator = PaginatorHandler(max(len(current_dir.children),
										 len(current_dir.cards)),
									 int(page),
									 int(step),
									 8)
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
		redirect(f"view?dir_id={currDir.dir_id}")

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
		redirect(f"view?dir_id={currDir.parent_id}")

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	@authenticated
	def delete(self, dir_id: int, **kwargs):
		result = super(DirectoryController, self) \
			.delete(dir_id=dir_id, user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		currDir = result["model"]
		redirect("view?dir_id={}".format(currDir.parent_id))

	@expose("com/keksovmen/Controllers/xhtml/util/move.xhtml")
	@authenticated
	def move(self, dir_id: int, parent_id=-1, **kwargs):
		result = super().move(parent_id,
							  dir_id=dir_id,
							  user_id=session.get('u_id', None))
		if "form" in result.keys():
			return result
		redirect(f"view?dir_id={result['model'].parent_id}")

	def _getDefaultForm(self, **kwargs):
		form = Form()
		form.addField(
			FormField("title").addCheckCondition(
				checkNotZeroLength, zeroLengthMessage("Title"))
				.addCheckCondition(
				isAcceptableLength(TITLE_SIZE),
				wrongLengthMessage(TITLE_SIZE)))
		form.addField(FormField("description").addCheckCondition(
			isAcceptableLength(DESCRIPTION_SIZE),
			wrongLengthMessage(DESCRIPTION_SIZE)))
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

	def _updateMoveForm(self, form: Form, model: Directory, parent_id):
		form.parent_id.addCheckCondition(
			lambda v: Directory.isNameFree(
				model.title,
				parent_id,
				model.creator),
			"Such directory name already exists in selected parent dir")
		form.current_dir.setValue(model)
		form.postfix.setValue("")
		form.pageTitle.setValue("Move Directory")
		form.view_style.setValue("dir_holder")
		form.id_field.setValue("dir_id")
