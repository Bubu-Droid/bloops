import re

import pytest

from bloops.validator import validate_args


class TestValidateArgs:
    def test_invalid_args(self):
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""

        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                11,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert "Invalid argument provided" in str(context.value)
        assert "are the only valid" in str(context.value)

    def test_valid_args(self):
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""
        validate_args(
            text,
            11,
            re.compile(r"\[(asy)(.*?)\]"),
            ["src", "label", "width", "alt", "caption"],
        )

    def test_empty_args(self):
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello]some random stuff
[/asy]"""

        validate_args(
            text,
            11,
            re.compile(r"\[(asy)(.*?)\]"),
            ["src", "label", "width", "alt", "caption"],
        )

    def test_asy_without_src(self):
        text = r"""lorem [asy label=hello]some random stuff[/asy] lorem"""
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert 'Missing mandatory parameter "src' in str(context.value)

    def test_asy_without_label(self):
        text = r"""lorem [asy src=/home/bubu/meow.png]some random stuff[/asy] lorem"""
        with pytest.raises(ValueError) as context:
            _ = validate_args(
                text,
                6,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert 'Missing mandatory parameter "label' in str(context.value)

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
