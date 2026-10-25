from bloops.bloopser import _convert_tag_to_html
from bloops.vars import BBCODE_TAGS


class TestListTag:
    def test_without_type(self) -> None:
        text = r"""lorem [list]some random stuff[/list] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["list"][0],
            BBCODE_TAGS["list"][1],
        )
        assert (
            res
            == r"""<ul>
some random stuff
</ul>"""
        )

    def test_list_ul(self) -> None:
        text = r"""lorem [list type=ul]some random stuff[/list] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["list"][0],
            BBCODE_TAGS["list"][1],
        )
        assert (
            res
            == r"""<ul>
some random stuff
</ul>"""
        )

    def test_list_ol(self) -> None:
        text = r"""lorem [list type=ol]some random stuff[/list] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["list"][0],
            BBCODE_TAGS["list"][1],
        )
        assert (
            res
            == r"""<ol>
some random stuff
</ol>"""
        )

    def test_list_ul_with_valid_style(self) -> None:
        text = (
            r"""lorem [list type=ul style=disc]some random stuff[/list] lorem"""
        )
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["list"][0],
            BBCODE_TAGS["list"][1],
        )
        assert (
            res
            == r"""<ul style="list-style-type: disc;">
some random stuff
</ul>"""
        )

    def test_list_ol_with_valid_style(self) -> None:
        text = r"""lorem [list type=ol style=1]some random stuff[/list] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["list"][0],
            BBCODE_TAGS["list"][1],
        )
        assert (
            res
            == r"""<ol type="1">
some random stuff
</ol>"""
        )
