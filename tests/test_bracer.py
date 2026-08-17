import re

import pytest

from bloops.bracer import (
    get_close_delim_end_index,
    gobble_around_delim,
    gobble_inside_delim,
)


class TestGetCloseDelimEndIndex:
    def test_missing_open_delim(self):
        text = r"""meow
lorem [ay]some random stuff
[/asy]"""
        with pytest.raises(SyntaxError) as context:
            _ = get_close_delim_end_index(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
        assert context.type is SyntaxError
        assert "No opening delimiter at the current position." in str(
            context.value
        )
        assert "2:" in str(context.value)
        assert "[ay]" in str(context.value)

    def test_missing_closing_delim(self):
        text = r"""meow
lorem [asy]some random stuff
[asy]
asdf [/asy]"""

        with pytest.raises(SyntaxError) as context:
            _ = get_close_delim_end_index(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
        assert context.type is SyntaxError
        assert "Failed to find an opening pair for delimiter." in str(
            context.value
        )
        assert "4:" in str(context.value)
        assert "asdf [/asy]" in str(context.value)

    def test_close_delim_index(self):
        text = r"""meow
lorem [asy]some[asy] [asy]random stuff[/asy]
[/asy][/asy]"""

        assert (
            get_close_delim_end_index(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
            == len(text) - 1
        )


class TestGobbleInsideDelim:
    def test_check_inside_delim(self):
        text = r"""meow
lorem [asy]some[asy] [asy]random stuff[/asy]
[/asy]
[/asy]"""
        out_text = r"""some[asy] [asy]random stuff[/asy]
[/asy]
"""
        assert (
            gobble_inside_delim(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
            == out_text
        )

    def test_check_inside_empty_delim(self):
        text = r"""meow
lorem [asy][/asy]"""
        out_text = r""""""
        assert (
            gobble_inside_delim(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
            == out_text
        )


class TestGobbleAroundDelim:
    def test_check_around_delim(self):
        text = r"""meow
lorem [asy]some[asy] [asy]random stuff[/asy]
[/asy]
[/asy]
"""
        out_text = r"""[asy]some[asy] [asy]random stuff[/asy]
[/asy]
[/asy]"""
        assert (
            gobble_around_delim(
                text, 11, re.compile(r"\[(asy)(.*?)\]"), re.compile(r"\[/asy\]")
            )
            == out_text
        )
