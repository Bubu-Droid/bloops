from bloops.bloopser import _convert_tag_to_html
from bloops.vars import BBCODE_TAGS


class TestImgTag:
    def test_img(self) -> None:
        text = r"""lorem [img src=/home/bubu/meow.png][/img] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["img"][0],
            BBCODE_TAGS["img"][1],
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png">
</figure>"""
        )

    def test_img_with_width(self) -> None:
        text = r"""lorem [img src=/home/bubu/meow.png width=50][/img] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["img"][0],
            BBCODE_TAGS["img"][1],
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" style="width: 50%; height: auto;">
</figure>"""
        )

    def test_img_with_alt(self) -> None:
        text = r"""lorem [img src=/home/bubu/meow.png alt="hello kitty"][/img] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["img"][0],
            BBCODE_TAGS["img"][1],
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" alt="hello kitty">
</figure>"""
        )

    def test_img_with_caption(self) -> None:
        text = r"""lorem [img src=/home/bubu/meow.png caption="some random stuff"][/img] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["img"][0],
            BBCODE_TAGS["img"][1],
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png">
<figcaption>some random stuff</figcaption>
</figure>"""
        )

    def test_img_with_all(self) -> None:
        text = r"""lorem [img src=/home/bubu/meow.png width=50 alt="hello kitty" caption="some random stuff"][/img] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["img"][0],
            BBCODE_TAGS["img"][1],
        )
        assert (
            res
            == r"""<figure>
<img src="/home/bubu/meow.png" alt="hello kitty" style="width: 50%; height: auto;">
<figcaption>some random stuff</figcaption>
</figure>"""
        )
