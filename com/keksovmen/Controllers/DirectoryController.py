import sqlalchemy
import inspect
from tg import session, redirect, request
from tg.decorators import expose

from com.keksovmen.Controllers.AbstractController import AbstractController
from com.keksovmen.Model.ModelInit import *
from com.keksovmen.Model.Directory import *
from com.keksovmen.Model.User import User
from com.keksovmen.Util import Form, FormField
from com.keksovmen.Helpers.Helpers import checkNotZeroLength, zeroLengthMessage


class DirectoryController(AbstractController):

	@expose()
	def index(self):
		redirect("/dir/view")

	@expose("com/keksovmen/Controllers/xhtml/dir/directoryView.xhtml")
	def view(self, dir_id: int = 0):

		current_dir = ModelInit.session.query(Directory) \
			.filter(Directory.creator == session.get('u_id', None)) \
			.filter(Directory.dir_id == dir_id).first()
		# par = current_dir.parrent
		# cards = ModelInit.session.query(Card) \
		# 	.filter(Card.creator == session.get('u_id', None)) \
		# 	.filter(Card.dir_id == dir_id) \
		# 	.order_by(Card.modification_time.desc())
		# parent = Directory.getDirectory(dir_id, session.get('u_id', None))
		return dict(current_dir=current_dir)

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	def create(self, parent_id: int, title=None, description=None):
		result = super(DirectoryController, self).create(
			parent_id=int(parent_id),
			title=title,
			description=description)
		if "form" in result.keys():
			return result
		redirect("view?dir_id={}".format(result["model"].dir_id))

	# form = self._getCreateForm(**kwargs)
	# if request.method.lower() == "get" or not form.isFormValid():
	# 	return dict(form=form)
	#
	# dir = Directory(title=title,
	# 				description=description,
	# 				creator=session['u_id'],
	# 				dir_id=User.generateDirectoryId(session['u_id']),
	# 				parent_id=parent)
	# ModelInit.session.add(dir)
	# ModelInit.session.commit()
	# dir.updateModification()
	# redirect("view?dir_id={}".format(dir.dir_id))

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	def edit(self, dir_id: int, title=None, description=None):
		currDir = Directory.getDirectory(dir_id, session["u_id"])
		if request.method.lower() == "get":
			title = currDir.title
			description = currDir.description

		form = self._getEditForm(title, description, currDir)
		if request.method.lower() == "get" or not form.isFormValid():
			return dict(form=form)
		updateInstance(currDir, title=title, description=description)
		redirect("view?dir_id={}".format(
			currDir.parent.dir_id if currDir.parent else 0))

	@expose("com/keksovmen/Controllers/xhtml/dir/dir.xhtml")
	def delete(self, dir_id: int):
		currDir = Directory.getDirectory(dir_id, session["u_id"])
		form = self._getDeleteForm(currDir)
		if request.method.lower() == "get":
			return dict(form=form)
		ModelInit.session.delete(currDir)
		ModelInit.session.commit()
		redirect("view?dir_id={}".format(
			currDir.parent.dir_id if currDir.parent else 0))

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
		form.setValues(**kwargs)
		return form

	def _getCreateForm(self, parent_id, title, description) -> Form:
		form = self._getDefaultForm(title=title,
									description=description,
									parent_id=parent_id,
									pageTitle="Create directory",
									action="create",
									button="Create")
		form.title.addCheckCondition(
			lambda v: Directory.isNameFree(title, parent_id, session['u_id']),
			"Such title already exists in current directory")
		return form

	def _getEditForm(self, title, description, currDir: Directory) -> Form:
		form = self._getDefaultForm(title=title,
									description=description,
									dir_id=currDir.dir_id,
									pageTitle="Edit directory",
									action="edit",
									button="Save")
		form.title.addCheckCondition(
			lambda v: currDir.isEditTitleFree(title),
			"Such title already exists in current directory")
		return form

	def _getDeleteForm(self, dir: Directory) -> Form:
		form = self._getDefaultForm(title=dir.title,
									description=dir.description,
									dir_id=dir.dir_id,
									pageTitle="Delete directory",
									action="delete",
									button="Delete")
		form.addField(FormField("dir", dir))
		return form

	def _createModelObject(self, parent_id, title, description):
		return Directory(title=title,
						 description=description,
						 creator=session['u_id'],
						 dir_id=User.generateDirectoryId(session['u_id']),
						 parent_id=parent_id)
