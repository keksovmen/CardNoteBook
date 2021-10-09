import math
from typing import Final

import webhelpers2
from webhelpers2.html.builder import HTMLBuilder
from com.keksovmen.Model.Directory import Directory
from functools import reduce
from html import unescape


def createBackNavigation(dir: Directory, isCardView: bool = False) -> str:
	builder = HTMLBuilder()
	result = [builder.tag("strong", _closed=False)]
	for index, parent in enumerate(reversed(dir.getParents())):
		if index != 0:
			result.append(" \ ")
		result.append(__getHrefTag(parent))
	if len(result) > 1:
		result.append(" \ ")
	if isCardView:
		result.append(__getHrefTag(dir))
	else:
		result.append(__getSpanTag(dir))
	result.append(builder.tag("/strong", _closed=False))
	return builder.tag("div", reduce(lambda t, v: t + v, result),
					   class_="back_navigation")


def createBackNavigationFromId(dir_id: int,
							   user_id: int,
							   isCardView: bool) -> str:
	return createBackNavigation(Directory.getDirectory(dir_id,
													   user_id),
								isCardView)


def checkNotZeroLength(value) -> bool:
	return isinstance(value, str) and len(value) != 0


def zeroLengthMessage(fieldName: str) -> str:
	return f"{fieldName} must contain at least 1 symbol"


def prettyTime(datetime):
	return datetime.strftime("%d.%m.%Y %H:%M")


def __getHrefTag(dir: Directory) -> webhelpers2.html.literal:
	return HTMLBuilder().tag("a", unescape(f"{dir.title}"),
							 href=f"/dir/view?dir_id={dir.dir_id}")


def __getSpanTag(dir: Directory) -> webhelpers2.html.literal:
	return HTMLBuilder().tag("span", unescape(f"{dir.title}"))


class PaginatorHandler:
	sourceLength: Final[int]
	page: Final[int]
	step: Final[int]
	amount: Final[int]

	def __init__(self, sourceLength, page=0, step=3, amount=5) -> None:
		self.sourceLength = sourceLength
		if page < 0:
			page = 0
		self.page = page
		if step <= 0:
			step = 1
		self.step = step
		if amount <= 0:
			amount = 5
		self.amount = amount

		possibleLeftAndSpare = self._findMaximumAndSparePages(
			self._getLeftPages(),
			self._getPossibleLeftPages(),
			0)
		possibleRightAndSpare = self._findMaximumAndSparePages(
			self._getRightPages(),
			self._getPossibleRightPages(),
			possibleLeftAndSpare[1])
		possibleRightAndSpare = self._distributeSpare(
			self._getRightPages(),
			possibleRightAndSpare[0],
			possibleRightAndSpare[1])
		possibleLeftAndSpare = self._distributeSpare(
			self._getLeftPages(),
			possibleLeftAndSpare[0],
			possibleRightAndSpare[1])
		self._possibleLeft = possibleLeftAndSpare[0]
		self._possibleRight = possibleRightAndSpare[0]

	def getIndexes(self):
		if self.page == 0 and self.step >= self.sourceLength:
			return []
		return [x for x in range(self.page - self._possibleLeft,
								 self.page + self._possibleRight + 1)]

	def _getLeftPages(self):
		return self.page

	def _getRightPages(self):
		return int(math.ceil(self.sourceLength / self.step)) - (self.page + 1)

	def _getPossibleLeftPages(self):
		return int(math.floor(self._getHalf()))

	def _getPossibleRightPages(self):
		return int(math.ceil(self._getHalf()))

	def _getHalf(self):
		return (self.amount - 1) / 2

	def _findMaximumAndSparePages(self, maximum, possible, sparePages):
		if maximum < possible:
			sparePages += possible - maximum
			possible = maximum
			sparePages = self._normalizeSparePages(sparePages)
		return possible, sparePages

	def _distributeSpare(self, maximum, possible, sparePages):
		if maximum > possible:
			if sparePages > maximum - possible:
				sparePages -= maximum - possible
				possible = maximum
			else:
				possible += sparePages
				sparePages = 0
		return possible, sparePages

	def _normalizeSparePages(self, sparePages):
		return 0 if sparePages < 0 else sparePages
