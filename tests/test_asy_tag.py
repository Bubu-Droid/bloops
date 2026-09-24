import re

from bloops.bloopser import _convert_tag_to_html


class TestImgTag:
    def test_asy(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png label=meow]some random stuff[/asy] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png">
</figure>"""
        )

    def test_asy_with_width(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png label=meow width=50]some random stuff[/asy] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" style="width: 50%; height: auto;">
</figure>"""
        )

    def test_asy_with_alt(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png label=meow alt="hello kitty"]some random stuff[/asy] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" alt="hello kitty">
</figure>"""
        )

    def test_asy_with_caption(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png label=meow caption="some caption"]some random stuff[/asy] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png">
<figcaption>some caption</figcaption>
</figure>"""
        )

    def test_asy_with_all(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png width=50 alt="hello kitty" caption="caption stuff"]some random stuff[/asy] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" alt="hello kitty" style="width: 50%; height: auto;">
<figcaption>caption stuff</figcaption>
</figure>"""
        )
