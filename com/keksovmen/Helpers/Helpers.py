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
