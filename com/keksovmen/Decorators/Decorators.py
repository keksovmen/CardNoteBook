import heapq

from tg import redirect, session

from com.keksovmen.Model.User import User

__all__ = ["authenticated", "asHeap"]


def authenticated(func):
	def aut(*args, **kwargs):
		if User.isAuthenticated(session.get('u_id', None)):
			return func(*args, **kwargs)
		redirect("/user/")

	return aut


def asHeap(func):
	def h(*args, **kwargs):
		initial = func(*args, **kwargs)
		result = []
		for i in initial:
			heapq.heappush(result, i)
		return result

	return h
