import re

# TODO: handle the case when there is a ] inside the string
# TODO: maybe convert this into a dict to not hardcode re.Pattern(s)
# in tests
BBCODE_TAGS: list[tuple[re.Pattern[str], re.Pattern[str], list[str]]] = [
    (
        re.compile(r"\[(asy)(.*?)\]"),
        re.compile(r"\[/asy\]"),
        ["src", "label", "width", "alt", "caption"],
    ),
    (re.compile(r"\[(code)(.*?)\]"), re.compile(r"\[/code\]"), ["lang"]),
    (re.compile(r"\[(color)(.*?)\]"), re.compile(r"\[/color\]"), ["hex"]),
    (
        re.compile(r"\[(img)(.*?)\]"),
        re.compile(r"\[/img\]"),
        ["width", "alt", "caption"],
    ),
    (
        re.compile(r"\[(list)(.*?)\]"),
        re.compile(r"\[/list\]"),
        ["type", "style"],
    ),
    (
        re.compile(r"\[(quote)(.*?)\]"),
        re.compile(r"\[/quote\]"),
        ["author", "link"],
    ),
    (
        re.compile(r"\[(url)(.*?)\]"),
        re.compile(r"\[/url\]"),
        ["link", "target"],
    ),
    (re.compile(r"\[(theorem)(.*?)\]"), re.compile(r"\[/theorem\]"), ["title"]),
    (re.compile(r"\[(lemma)(.*?)\]"), re.compile(r"\[/lemma\]"), ["title"]),
    (
        re.compile(r"\[(proposition)(.*?)\]"),
        re.compile(r"\[/proposition\]"),
        ["title"],
    ),
    (
        re.compile(r"\[(corollary)(.*?)\]"),
        re.compile(r"\[/corollary\]"),
        ["title"],
    ),
    (re.compile(r"\[(example)(.*?)\]"), re.compile(r"\[/example\]"), ["title"]),
    (re.compile(r"\[(claim)(.*?)\]"), re.compile(r"\[/claim\]"), ["title"]),
    (re.compile(r"\[(problem)(.*?)\]"), re.compile(r"\[/problem\]"), ["title"]),
    (
        re.compile(r"\[(exercise)(.*?)\]"),
        re.compile(r"\[/exercise\]"),
        ["title"],
    ),
    (re.compile(r"\[(b)\]"), re.compile(r"\[/b\]"), []),
    (re.compile(r"\[(i)\]"), re.compile(r"\[/i\]"), []),
    (re.compile(r"\[(u)\]"), re.compile(r"\[/u\]"), []),
    (re.compile(r"\[(s)\]"), re.compile(r"\[/s\]"), []),
    (re.compile(r"\[(\*)\]"), re.compile(r"\[/\*\]"), []),
    (re.compile(r"\[(sub)\]"), re.compile(r"\[/sub\]"), []),
    (re.compile(r"\[(sup)\]"), re.compile(r"\[/sup\]"), []),
    (re.compile(r"\[(proof)\]"), re.compile(r"\[/proof\]"), []),
    (re.compile(r"\[(soln)\]"), re.compile(r"\[/soln\]"), []),
]
