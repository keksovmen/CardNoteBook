import math
from typing import Final


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

	def hasBeginningPage(self):
		return self.page != 0

	def hasEndPage(self):
		return self._getSourceLengthInPages() != self.page + 1

	def getBeginningIndex(self):
		return 0

	def getEndIndex(self):
		return self._getSourceLengthInPages() - 1

	def _getLeftPages(self):
		return self.page

	def _getRightPages(self):
		return self._getSourceLengthInPages() - (self.page + 1)

	def _getSourceLengthInPages(self):
		return int(math.ceil(self.sourceLength / self.step))

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