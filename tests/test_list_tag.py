import re

import pytest

from bloops.bloopser import convert_to_html


class TestListTag:
    def test_without_type(self):
        text = r"""lorem [list]some random stuff[/list] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(list)(.*?)\]"),
            re.compile(r"\[/list\]"),
        )
        assert (
            res
            == r"""<ul>
some random stuff
</ul>"""
        )

    def test_list_ul(self):
        text = r"""lorem [list type=ul]some random stuff[/list] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(list)(.*?)\]"),
            re.compile(r"\[/list\]"),
        )
        assert (
            res
            == r"""<ul>
some random stuff
</ul>"""
        )

    def test_list_ol(self):
        text = r"""lorem [list type=ol]some random stuff[/list] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(list)(.*?)\]"),
            re.compile(r"\[/list\]"),
        )
        assert (
            res
            == r"""<ol>
some random stuff
</ol>"""
        )

    def test_list_ul_with_invalid_style(self):
        text = (
            r"""lorem [list type=ul style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = convert_to_html(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                re.compile(r"\[/list\]"),
            )
        assert context.type is ValueError
        assert "Invalid <ul> style provided" in str(context.value)

    def test_list_ol_with_invalid_style(self):
        text = (
            r"""lorem [list type=ol style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = convert_to_html(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                re.compile(r"\[/list\]"),
            )
        assert context.type is ValueError
        assert "Invalid <ol> style provided" in str(context.value)

    def test_list_ul_with_valid_style(self):
        text = (
            r"""lorem [list type=ul style=disc]some random stuff[/list] lorem"""
        )
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(list)(.*?)\]"),
            re.compile(r"\[/list\]"),
        )
        assert (
            res
            == r"""<ul style="list-style-type: disc;">
some random stuff
</ul>"""
        )

    def test_list_ol_with_valid_style(self):
        text = r"""lorem [list type=ol style=1]some random stuff[/list] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(list)(.*?)\]"),
            re.compile(r"\[/list\]"),
        )
        assert (
            res
            == r"""<ol type="1">
some random stuff
</ol>"""
        )
