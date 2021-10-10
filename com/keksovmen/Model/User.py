from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc

from com.keksovmen.Model.Card import Card
from com.keksovmen.Model.Constants import USER_NAME_SIZE, USER_PASSWORD_SIZE
from com.keksovmen.Model.Directory import Directory
from com.keksovmen.Model.ModelInit import ModelInit

__all__ = ["User"]


class User(ModelInit.DeclarativeBase):
	__tablename__ = "users"

	u_id = Column(type_=Integer, primary_key=True, autoincrement=True)
	name = Column(type_=String(USER_NAME_SIZE), nullable=False, unique=True)
	password = Column(type_=String(USER_PASSWORD_SIZE), nullable=False)
	reg_time = Column(type_=DateTime, nullable=False, default=datetime.now)
	owned_dirs = Column(type_=Integer, default=0)
	owned_cards = Column(type_=Integer, default=0)

	dirs = relationship("Directory",
						order_by=desc(Directory.creation_time),
						# back_populates="user",
						cascade="all, delete, delete-orphan")

	cards = relationship("Card",
						 order_by=desc(Card.creation_time),
						 cascade="all, delete, delete-orphan")

	def isEditNameFree(self, name):
		return ModelInit.session.query(User) \
				   .filter(User.name == name) \
				   .filter(User.u_id != self.u_id) \
				   .count() == 0

	@staticmethod
	def generateDirectoryId(user_id):
		'''
			Don't forget commit changes to session
			:param user_id:
			:return:
		'''
		user = ModelInit.session.query(User).filter(
			User.u_id == user_id).first()
		if not user:
			raise ValueError
		user.owned_dirs += 1
		return user.owned_dirs

	@staticmethod
	def generateCardId(user_id):
		'''
			Don't forget commit changes to session
			:param user_id:
			:return:
		'''
		user = ModelInit.session.query(User).filter(
			User.u_id == user_id).first()
		if not user:
			raise ValueError
		user.owned_cards += 1
		return user.owned_cards

	@staticmethod
	def isNameFree(name: str) -> bool:
		return ModelInit.session.query(User).filter(
			User.name == name).count() == 0

	@staticmethod
	def getMe(user_id):
		return ModelInit.session.query(User).filter(
			User.u_id == user_id).first()

	@staticmethod
	def isAuthenticated(user_id):
		if not user_id:
			return False
		return True
