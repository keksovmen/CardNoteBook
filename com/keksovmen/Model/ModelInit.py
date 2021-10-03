from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ModelInit:
	session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
	DeclarativeBase = declarative_base()

	@staticmethod
	def init_model(engine):
		ModelInit.session.configure(bind=engine)
		ModelInit.DeclarativeBase.metadata.create_all(engine)


def updateInstance(instance: object, **kwargs):
	for k, v in kwargs.items():
		setattr(instance, k, v)
	ModelInit.session.commit()
