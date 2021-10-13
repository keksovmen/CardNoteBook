from datetime import datetime
from hashlib import scrypt
from os import urandom
from typing import Tuple

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from com.keksovmen.Model.Constants import USER_NAME_SIZE, SALT_SIZE, \
	HASHED_PASS_SIZE
from com.keksovmen.Model.ModelInit import ModelInit

__all__ = ["User"]


class User(ModelInit.DeclarativeBase):
	__tablename__ = "users"

	u_id = Column(type_=Integer, primary_key=True, autoincrement=True)
	name = Column(type_=String(USER_NAME_SIZE), nullable=False, unique=True)
	salt = Column(type_=String(SALT_SIZE), nullable=False, unique=True)
	hash_pass = Column(type_=String(HASHED_PASS_SIZE), nullable=False)
	reg_time = Column(type_=DateTime, nullable=False, default=datetime.now)
	owned_dirs = Column(type_=Integer, default=0)
	owned_cards = Column(type_=Integer, default=0)

	dirs = relationship("Directory",
						order_by="desc(Directory.creation_time)",
						# back_populates="user",
						cascade="all, delete, delete-orphan")

	cards = relationship("Card",
						 order_by="desc(Card.creation_time)",
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

	@staticmethod
	def isPasswordCorrect(name: str, password: str):
		user = ModelInit.session.query(User) \
			.filter(User.name == name).first()
		return user.hash_pass == \
			   User.generateSaltedHashPass(password, user.salt)

	@staticmethod
	def generateSalt() -> str:
		salt = urandom(int(SALT_SIZE / 2)).hex()
		while salt in ModelInit.session.query(User.salt).all():
			salt = urandom(int(SALT_SIZE / 2)).hex()
		return salt

	@staticmethod
	def generateSaltedHashPass(password: str, salt: str) -> str:
		return scrypt(bytes(password, "utf-8"),
					  salt=bytes(salt, "utf-8"),
					  n=8,
					  r=64,
					  p=2,
					  dklen=int(HASHED_PASS_SIZE / 2)).hex()

	@staticmethod
	def generateSaltPassPair(password: str) -> Tuple[str, str]:
		salt = User.generateSalt()
		return salt, User.generateSaltedHashPass(password, salt)
