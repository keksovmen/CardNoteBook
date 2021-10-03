from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, Text
from sqlalchemy.orm import relationship, backref
from com.keksovmen.Model.ModelInit import ModelInit

from datetime import datetime


class Card(ModelInit.DeclarativeBase):
	__tablename__ = "cards"

	card_id = Column(Integer, nullable=False)
	title = Column(String(256), nullable=False)
	description = Column(String(1024), nullable=True)
	message = Column(Text, nullable=True)
	creation_time = Column(DateTime, default=datetime.now)
	modification_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
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
