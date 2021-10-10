from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, \
	UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc

from com.keksovmen.Model.Card import Card
from com.keksovmen.Model.Constants import TITLE_SIZE, DESCRIPTION_SIZE
from com.keksovmen.Model.ModelInit import ModelInit

__all__ = ["Directory"]


class Directory(ModelInit.DeclarativeBase):
	__tablename__ = "directories"

	dir_id = Column(Integer, nullable=False)
	title = Column(String(TITLE_SIZE), nullable=False)
	description = Column(String(DESCRIPTION_SIZE), nullable=True)
	creator = Column(Integer, ForeignKey("users.u_id"), nullable=False)
	creation_time = Column(DateTime, default=datetime.now)
	modification_time = Column(DateTime,
							   default=datetime.now,
							   onupdate=datetime.now)
	parent_id = Column(Integer, ForeignKey("directories.dir_id"))

	UniqueConstraint(creator, title, parent_id)
	PrimaryKeyConstraint(dir_id, creator)

	parent = relationship("Directory",
						  primaryjoin="and_(Directory.dir_id==Directory.parent_id, "
									  "Directory.creator==Directory.creator)",
						  remote_side=[dir_id, creator],
						  back_populates="children")
	children = relationship("Directory",
							primaryjoin="and_(Directory.dir_id==Directory.parent_id, "
										"Directory.creator==Directory.creator)",
							remote_side=[parent_id, creator],
							cascade="all, delete, delete-orphan",
							order_by=desc(modification_time),
							back_populates="parent")

	# user = relationship("User", back_populates="dirs")
	cards = relationship("Card",
						 primaryjoin="and_(Directory.dir_id==Card.dir_id, "
									 "Directory.creator==Card.creator)",
						 back_populates="parent_dir",
						 order_by=desc(Card.modification_time),
						 cascade="all, delete, delete-orphan")

	@staticmethod
	def isNameFree(title: str, parent_id: int, creator_id: int) -> bool:
		return ModelInit.session.query(Directory) \
				   .filter(Directory.title == title) \
				   .filter(Directory.parent_id == parent_id) \
				   .filter(Directory.creator == creator_id) \
				   .count() == 0

	@staticmethod
	def getDirectory(dir_id: int, creator_id: int) -> Directory:
		return ModelInit.session.query(Directory) \
			.filter(Directory.dir_id == dir_id) \
			.filter(Directory.creator == creator_id).first()

	def isEditTitleFree(self, newTitle: str) -> bool:
		return ModelInit.session.query(Directory) \
				   .filter(Directory.title == newTitle) \
				   .filter(Directory.parent_id == self.parent_id) \
				   .filter(Directory.creator == self.creator) \
				   .filter(Directory.dir_id != self.dir_id) \
				   .count() == 0

	def countSubDirs(self) -> int:
		result = len(self.children)
		for c in self.children:
			result += c.countSubDirs()
		return result

	def countCards(self) -> int:
		result = len(self.cards)
		for c in self.children:
			result += c.countCards()
		return result

	def getParents(self) -> List[Directory]:
		parents = []
		par = self.parent
		while par:
			parents.append(par)
			par = par.parent
		return parents

	def updateModification(self):
		self.modification_time = datetime.now()
		if self.parent:
			self.parent.updateModification()
		else:
			ModelInit.session.commit()
