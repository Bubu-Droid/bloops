import re

import pytest

from bloops.bloopser import get_tag_and_args, validate_args


class TestGetTagAndArgs:
    def test_missing_open_delim(self):
        text = r"""meow
lorem [ay]some random stuff
[/asy]"""
        with pytest.raises(SyntaxError) as context:
            _ = get_tag_and_args(text, 11, re.compile(r"\[(asy)(.*?)\]"))
        assert context.type is SyntaxError
        assert "No opening delimiter at the current position." in str(
            context.value
        )

    def test_simple_tag(self):
        text = r"""meow lorem [b]some random stuff[/b]"""
        res = get_tag_and_args(text, 11, re.compile(r"\[(b)\]"))
        assert res[0] == "b"
        assert res[1] == {}

    def test_no_args(self):
        text = r"""meow
lorem [asy]some random stuff
[/asy]"""
        res = get_tag_and_args(text, 11, re.compile(r"\[(asy)(.*?)\]"))
        assert res[0] == "asy"
        assert res[1] == {}

    def test_args(self):
        text = r"""meow
lorem [asy meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""
        res = get_tag_and_args(text, 11, re.compile(r"\[(asy)(.*?)\]"))
        assert res[0] == "asy"
        assert res[1] == {
            "meow": "hi",
            "width": "50",
            "alt": "meow neow",
            "caption": "this",
        }


class TestValidateArgs:
    def test_simple_tag(self):
        text = r"""meow lorem [b]some random stuff[/b]"""
        res = validate_args(text, 11, re.compile(r"\[(b)\]"), [])
        assert res == False

    def test_invalid_args(self):
        text = r"""meow
lorem [asy meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""

        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                11,
                re.compile(r"\[(asy)(.*?)\]"),
                ["width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert "Invalid argument provided" in str(context.value)
        assert "are the only valid" in str(context.value)

    def test_valid_args(self):
        text = r"""meow
lorem [asy width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""

        res = validate_args(
            text, 11, re.compile(r"\[(asy)(.*?)\]"), ["width", "alt", "caption"]
        )

        assert res is True

    def test_empty_args(self):
        text = r"""meow
lorem [asy]some random stuff
[/asy]"""

        res = validate_args(
            text, 11, re.compile(r"\[(asy)(.*?)\]"), ["width", "alt", "caption"]
        )

        assert res is False

    def test_img_without_src(self):
        text = r"""lorem [img]some random stuff[/img] lorem"""

        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(img)(.*?)\]"),
                ["width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_list_ul_with_invalid_style(self):
        text = (
            r"""lorem [list type=ul style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                ["type", "style"],
            )
        assert context.type is ValueError
        assert "Invalid <ul> style provided" in str(context.value)

    def test_list_ol_with_invalid_style(self):
        text = (
            r"""lorem [list type=ol style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                ["type", "style"],
            )
        assert context.type is ValueError
        assert "Invalid <ol> style provided" in str(context.value)

    def test_color_without_hex(self):
        text = r"""lorem [color]some random stuff[/color] lorem"""
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(color)(.*?)\]"),
                ["hex"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_url_without_link(self):
        text = r"""lorem [url]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                ["link", "target"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_url_with_invalid_target(self):
        text = r"""lorem [url link=https://www.bubudroid.me target=meow]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                ["link", "target"],
            )
        assert context.type is ValueError
        assert "Invalid target value provided" in str(context.value)
