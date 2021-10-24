from functools import reduce
from html import unescape

import webhelpers2
from webhelpers2.html.builder import HTMLBuilder

from com.keksovmen.Model.Directory import Directory

__all__ = ["createBackNavigation",
		   "createBackNavigationFromId",
		   "checkNotZeroLength",
		   "zeroLengthMessage",
		   "prettyTime",
		   "isAcceptableLength",
		   "wrongLengthMessage",
		   "webhelpers2",
		   "createDirTree"]


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


def isAcceptableLength(max_size: int):
	def wrapper(value: str) -> bool:
		return len(value) <= max_size

	return wrapper


def wrongLengthMessage(max_size: int) -> str:
	return f"Field length must be less or equal to {max_size} symbols"


def createDirTree(root: Directory, current: Directory) -> str:
	builder = HTMLBuilder()
	result = [__getTreeTag(root, current, False)]
	result.append(builder.tag("ul", _closed=False, class_="tree"))
	result.extend([__createTreeNode(child, current) for child in root.children])
	result.append(builder.tag("/ul", _closed=False))

	return reduce(lambda t, v: t + v, result)


def __createTreeNode(directory: Directory, current: Directory) -> str:
	# TODO: use htmlbuilder to make it in 1 call without using an intermidiet list
	if directory.children:
		builder = HTMLBuilder()
		result = [builder.tag("li", _closed=False),
				  builder.tag("span", "", class_="caret"),
				  __wrapTag(__getTreeTag(directory, current), "span",
							"parent_node"),
				  builder.tag("ul", _closed=False, class_="child_node")]
		for child in directory.children:
			result.append(__createTreeNode(child, current))
		result.append(builder.tag("/ul", _closed=False))
		result.append(builder.tag("/li", _closed=False))
		return reduce(lambda t, v: t + v, result)
	else:
		return __wrapTag(__getTreeTag(directory, current), "li")


def __getHrefTag(dir: Directory) -> webhelpers2.html.literal:
	return HTMLBuilder().tag("a", unescape(f"{dir.title}"),
							 href=f"/dir/view?dir_id={dir.dir_id}")


def __getSpanTag(dir: Directory) -> webhelpers2.html.literal:
	return HTMLBuilder().tag("span", f"{dir.title}")


def __getTreeTag(dir: Directory, cur_dir: Directory, enableId: bool = True):
	createFunc = __getSpanTag if dir == cur_dir else __getHrefTag
	if enableId:
		return __wrapTag(createFunc(dir),
						 "span",
						 parentId="current_dir" if dir == cur_dir else None)
	else:
		return createFunc(dir)


def __wrapTag(tagToWrap, parentTag,
			  parentClass=None, parentId=None) -> webhelpers2.html.literal:
	return HTMLBuilder().tag(parentTag, tagToWrap, class_=parentClass,
							 id=parentId)
