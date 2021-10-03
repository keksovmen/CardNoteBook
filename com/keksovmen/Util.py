from typing import Callable, Union, List, Dict, Any, Final, Tuple


class FormField:
	name: Final[str]

	def __init__(self, name: str, value=None) -> None:
		self.name = name
		self._value = value
		self._conditions = []
		self._error = ""

	def addCheckCondition(self, func: Callable[[object], bool], errMes: str):
		self._conditions.append((func, errMes))
		return self

	def isFieldValid(self) -> bool:
		self._cleanError()
		for cond, err in self._conditions:
			result = cond(self._value)
			if not result:
				self._error = err
				return False
		return True

	def getError(self) -> str:
		return self._error

	def getValue(self):
		return self._value

	def setValue(self, value):
		self._value = value

	def _cleanError(self):
		self._error = ""


class Form:
	fields: Dict[str, FormField]

	def __init__(self) -> None:
		self.fields = {}

	def addField(self, field: FormField) -> None:
		self.fields[field.name] = field

	def isFormValid(self) -> bool:
		for f in self.fields.values():
			if not f.isFieldValid():
				return False
		return True

	def setValues(self, **kwargs):
		for k, v in kwargs.items():
			self.fields[k].setValue(v)

	def __getattr__(self, item):
		return self.fields[item]

	def __getitem__(self, item):
		return self.fields[item]


