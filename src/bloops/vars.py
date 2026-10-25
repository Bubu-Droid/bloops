"""Definitions of the BBCode tags supported by bloops."""

import re

BBCODE_TAGS: dict[str, tuple[re.Pattern[str], re.Pattern[str], list[str]]] = {
    "asy": (
        re.compile(r"\[(asy)(.*?)\]"),
        re.compile(r"\[/asy\]"),
        ["src", "label", "width", "alt", "caption"],
    ),
    "code": (
        re.compile(r"\[(code)(.*?)\]"),
        re.compile(r"\[/code\]"),
        ["lang"],
    ),
    "color": (
        re.compile(r"\[(color)(.*?)\]"),
        re.compile(r"\[/color\]"),
        ["hex"],
    ),
    "img": (
        re.compile(r"\[(img)(.*?)\]"),
        re.compile(r"\[/img\]"),
        ["src", "width", "alt", "caption"],
    ),
    "list": (
        re.compile(r"\[(list)(.*?)\]"),
        re.compile(r"\[/list\]"),
        ["type", "style"],
    ),
    "quote": (
        re.compile(r"\[(quote)(.*?)\]"),
        re.compile(r"\[/quote\]"),
        ["author", "link"],
    ),
    "url": (
        re.compile(r"\[(url)(.*?)\]"),
        re.compile(r"\[/url\]"),
        ["link", "target"],
    ),
    "hide": (
        re.compile(r"\[(hide)(.*?)\]"),
        re.compile(r"\[/hide\]"),
        ["label"],
    ),
    "theorem": (
        re.compile(r"\[(theorem)(.*?)\]"),
        re.compile(r"\[/theorem\]"),
        ["title"],
    ),
    "lemma": (
        re.compile(r"\[(lemma)(.*?)\]"),
        re.compile(r"\[/lemma\]"),
        ["title"],
    ),
    "proposition": (
        re.compile(r"\[(proposition)(.*?)\]"),
        re.compile(r"\[/proposition\]"),
        ["title"],
    ),
    "corollary": (
        re.compile(r"\[(corollary)(.*?)\]"),
        re.compile(r"\[/corollary\]"),
        ["title"],
    ),
    "example": (
        re.compile(r"\[(example)(.*?)\]"),
        re.compile(r"\[/example\]"),
        ["title"],
    ),
    "claim": (
        re.compile(r"\[(claim)(.*?)\]"),
        re.compile(r"\[/claim\]"),
        ["title"],
    ),
    "problem": (
        re.compile(r"\[(problem)(.*?)\]"),
        re.compile(r"\[/problem\]"),
        ["title"],
    ),
    "exercise": (
        re.compile(r"\[(exercise)(.*?)\]"),
        re.compile(r"\[/exercise\]"),
        ["title"],
    ),
    "b": (re.compile(r"\[(b)\]"), re.compile(r"\[/b\]"), []),
    "i": (re.compile(r"\[(i)\]"), re.compile(r"\[/i\]"), []),
    "u": (re.compile(r"\[(u)\]"), re.compile(r"\[/u\]"), []),
    "s": (re.compile(r"\[(s)\]"), re.compile(r"\[/s\]"), []),
    "*": (re.compile(r"\[(\*)\]"), re.compile(r"\[/\*\]"), []),
    "sub": (re.compile(r"\[(sub)\]"), re.compile(r"\[/sub\]"), []),
    "sup": (re.compile(r"\[(sup)\]"), re.compile(r"\[/sup\]"), []),
    "sidemark": (
        re.compile(r"\[(sidemark)\]"),
        re.compile(r"\[/sidemark\]"),
        [],
    ),
    "sidenote": (
        re.compile(r"\[(sidenote)\]"),
        re.compile(r"\[/sidenote\]"),
        [],
    ),
    "proof": (re.compile(r"\[(proof)\]"), re.compile(r"\[/proof\]"), []),
    "soln": (re.compile(r"\[(soln)\]"), re.compile(r"\[/soln\]"), []),
    "h1": (re.compile(r"\[(h1)\]"), re.compile(r"\[/h1\]"), []),
    "h2": (re.compile(r"\[(h2)\]"), re.compile(r"\[/h2\]"), []),
    "h3": (re.compile(r"\[(h3)\]"), re.compile(r"\[/h3\]"), []),
    "h4": (re.compile(r"\[(h4)\]"), re.compile(r"\[/h4\]"), []),
    "h5": (re.compile(r"\[(h5)\]"), re.compile(r"\[/h5\]"), []),
    "h6": (re.compile(r"\[(h6)\]"), re.compile(r"\[/h6\]"), []),
}
"""Mapping of each tag name to `(open_pattern, close_pattern, valid_args)`.

- `open_pattern` matches the opening tag. Group 1 captures the tag name
  and, for tags that take arguments, group 2 captures the raw argument
  string.
- `close_pattern` matches the closing tag.
- `valid_args` lists the argument names the tag accepts, and is empty
  for tags without arguments.

Tags are processed in the order they appear here.
"""
