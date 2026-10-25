import pytest

from bloops._helper import get_tag_and_args
from bloops.vars import BBCODE_TAGS


class TestGetTagAndArgs:
    def test_missing_open_delim(self) -> None:
        text = r"""meow
lorem [ay]some random stuff
[/asy]"""
        with pytest.raises(SyntaxError) as context:
            _ = get_tag_and_args(text, 11, BBCODE_TAGS["asy"][0])
        assert context.type is SyntaxError
        assert "No opening delimiter at the current position." in str(
            context.value
        )

    def test_simple_tag(self) -> None:
        text = r"""meow lorem [b]some random stuff[/b]"""
        res = get_tag_and_args(text, 11, BBCODE_TAGS["b"][0])
        assert res[0] == "b"
        assert res[1] == {}

    def test_no_args(self) -> None:
        text = r"""meow
lorem [asy]some random stuff
[/asy]"""
        res = get_tag_and_args(text, 11, BBCODE_TAGS["asy"][0])
        assert res[0] == "asy"
        assert res[1] == {}

    def test_args(self) -> None:
        text = r"""meow
lorem [asy meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""
        res = get_tag_and_args(text, 11, BBCODE_TAGS["asy"][0])
        assert res[0] == "asy"
        assert res[1] == {
            "meow": "hi",
            "width": "50",
            "alt": "meow neow",
            "caption": "this",
        }
