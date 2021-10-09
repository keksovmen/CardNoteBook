from tg import redirect, session
from com.keksovmen.Model.User import User


def authenticated(func):
	def aut(*args, **kwargs):
		if User.isAuthenticated(session.get('u_id', None)):
			return func(*args, **kwargs)
		redirect("/user/")

	return aut
