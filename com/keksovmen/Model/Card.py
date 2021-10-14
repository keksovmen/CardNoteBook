from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, \
	UniqueConstraint, PrimaryKeyConstraint, Text
from sqlalchemy.orm import relationship

from com.keksovmen.Model.Constants import TITLE_SIZE, DESCRIPTION_SIZE, \
	TEXT_SIZE
from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.ModelInit import ModelInit

__all__ = ["Card"]


class Card(ModelInit.DeclarativeBase):
	__tablename__ = "cards"

	card_id = Column(Integer, nullable=False)
	title = Column(String(TITLE_SIZE), nullable=False)
	description = Column(String(DESCRIPTION_SIZE), nullable=True)
	message = Column(Text(TEXT_SIZE), nullable=True)
	creation_time = Column(DateTime, default=datetime.now)
	modification_time = Column(DateTime, default=datetime.now,
							   onupdate=datetime.now)
	creator = Column(Integer, ForeignKey("users.u_id"), nullable=False)
	dir_id = Column(Integer, ForeignKey("directories.dir_id"), nullable=False)

	UniqueConstraint(creator, title, dir_id)
	PrimaryKeyConstraint(card_id, creator)

	parent_dir = relationship("Directory", back_populates="cards")

	@staticmethod
	def getCard(card_id: int, creator_id: int):
		return ModelInit.session.query(Card) \
			.filter(Card.card_id == card_id) \
			.filter(Card.creator == creator_id).first()

	@staticmethod
	def isNameFree(title: str, dir_id: int, creator_id: int):
		return ModelInit.session.query(Card) \
				   .filter(Card.title == title) \
				   .filter(Card.dir_id == dir_id) \
				   .filter(Card.creator == creator_id) \
				   .count() == 0

	def isEditTitleFree(self, newTitle: str):
		return ModelInit.session.query(Card) \
				   .filter(Card.title == newTitle) \
				   .filter(Card.dir_id == self.dir_id) \
				   .filter(Card.creator == self.creator) \
				   .filter(Card.card_id != self.card_id) \
				   .count() == 0

	def updateModification(self):
		self.modification_time = datetime.now()
		if self.parent_dir:
			self.parent_dir.updateModification()
		else:
			ModelInit.session.commit()

	def getPossibleParents(self):
		parents = ModelInit.session.query(Directory) \
			.filter(Directory.creator == self.creator) \
			.filter(Directory.dir_id != self.dir_id) \
			.all()
		parents.sort()
		return parents

	def move(self, new_dir_id):
		self.dir_id = new_dir_id
		ModelInit.session.commit()
		self.updateModification()

	def getId(self):
		return self.card_id

	def getParentId(self):
		return self.dir_id
