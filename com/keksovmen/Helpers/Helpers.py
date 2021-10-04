import webhelpers2
from webhelpers2.html.builder import HTMLBuilder
from com.keksovmen.Model.Directory import Directory
from functools import reduce
from html import unescape


def createBackNavigation(dir: Directory, appendCurrent: bool = False) -> str:
	builder = HTMLBuilder()
	result = []
	parents = dir.getParents()
	if appendCurrent:
		parents.insert(0, dir)
	for parent in reversed(parents):
		result.append(builder.tag("a", unescape(f"&larr;{parent.title}"),
								  href=f"/dir/view?dir_id={parent.dir_id}"))
	if not result:
		return ""
	return builder.tag("div", reduce(lambda t, v: t + v, result),
					   class_="back_navigation")


def checkNotZeroLength(value) -> bool:
	return isinstance(value, str) and len(value) != 0


def zeroLengthMessage(fieldName: str) -> str:
	return f"{fieldName} must contain at least 1 symbol"


def prettyTime(datetime):
	return datetime.strftime("%d.%m.%Y %H:%M")
