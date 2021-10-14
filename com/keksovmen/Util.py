from typing import Callable, Dict, Final

__all__ = ["Form", "FormField", "Globals"]


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

	def clearAllValidationChecks(self):
		self._conditions.clear()

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

	def clearAllValidationChecks(self):
		for f in self.fields.values():
			f.clearAllValidationChecks()

	def __getattr__(self, item):
		return self.fields[item]

	def __getitem__(self, item):
		return self.fields[item]


class Globals:
	_mappings = {'-p': 'port',
				 '-db': 'database',
				 '-dpp': 'dirPerPage',
				 '-scpd': 'subCardPerDir',
				 '-sc': 'sessionCache'
				 }

	def __init__(self,
				 port=8080,
				 database="database.db",
				 dirPerPage=4,
				 subCardPerDir=2,
				 sessionCache="cache/sessions/") -> None:
		self.port = port
		self.database = database
		self.dirPerPage = dirPerPage
		self.subCardPerDir = subCardPerDir
		self.sessionCache = sessionCache

	@staticmethod
	def createFromCommandLine(arguments: list):
		if not arguments:
			return Globals()
		pairs = dict(map(lambda t: (Globals._mappings[t[0]], t[1]),
						 Globals._validateArguments(arguments).items()))
		return Globals(**pairs)

	@staticmethod
	def functionCreateFromCommandLine(arguments: list):
		def f():
			return Globals.createFromCommandLine(arguments)

		return f

	@staticmethod
	def _validateArguments(arguments: list) -> dict:
		if len(arguments) % 2 != 0:
			raise ValueError("Argument list must have even length"
							 " containing -key value pairs")
		pairs = dict(zip(arguments[0::2], arguments[1::2]))
		for k in pairs.keys():
			if k not in Globals._mappings:
				raise IndexError(f"No such argument {k}")
		return pairs

	@staticmethod
	def allowedArguments():
		return f"Allowed arguments:\n" \
			   f"-p Port to bind on, > 0 < {2 ** 16 - 1}\n" \
			   f"-db Database path, must end with valid file .db\n" \
			   f"-dpp Amount of directories per page to display > 0\n" \
			   f"-scpd Amount card to display in next directory > 0\n" \
			   f"-sc Session cahce path"
