import pathlib
import re

from bloops.bracer import get_close_delim_end_index

# TODO: handle the case when there is a ] inside the string
# TODO: maybe convert this into a dict to not hardcode re.Pattern(s)
# in tests
BBCODE_TAGS = [
    (
        re.compile(r"\[(asy)(.*?)\]"),
        re.compile(r"\[/asy\]"),
        ["width", "alt", "caption"],
    ),
    (re.compile(r"\[b\]"), re.compile(r"\[/b\]")),
    (re.compile(r"\[i\]"), re.compile(r"\[/i\]")),
    (re.compile(r"\[u\]"), re.compile(r"\[/u\]")),
    (re.compile(r"\[s\]"), re.compile(r"\[/s\]")),
    (
        re.compile(r"\[(code)(.*?)\]"),
        re.compile(r"\[/code\]"),
        ["lang"],
    ),
    (
        re.compile(r"\[(color)(.*?)\]"),
        re.compile(r"\[/color\]"),
        ["hex"],
    ),
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
    (re.compile(r"\[\*\]"), re.compile(r"\[/\*\]")),
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
    (re.compile(r"\[sub\]"), re.compile(r"\[/sub\]")),
    (re.compile(r"\[sup\]"), re.compile(r"\[/sup\]")),
    (
        re.compile(r"\[theorem(.*?)\]"),
        re.compile(r"\[/theorem\]"),
        ["title"],
    ),
]


def main(path: pathlib.Path):
    ABS_PATH = path.absolute()
    validate(ABS_PATH)


def validate(path: pathlib.Path):
    file_path = path / "content.bbcode"
    if not file_path.exists():
        raise FileNotFoundError("BBCode file (content.bbcode) not found.")
    with file_path.open(mode="r", encoding="utf-8") as f:
        file_content = f.read().strip()

    for tag in BBCODE_TAGS:
        index = 0
        match = tag[0].search(file_content, index)
        while match:
            _ = get_close_delim_end_index(
                file_content,
                match.start(),
                tag[0],
                tag[1],
            )
            index = match.end()
            match = tag[0].search(file_content, index)
