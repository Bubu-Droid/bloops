import re

import pytest

from bloops.bloopser import convert_to_html, get_tag_and_args, validate_args


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

    def test_no_args(self):
        text = r"""meow
lorem [asy]some random stuff
[/asy]"""
        tag_and_args = get_tag_and_args(text, 11, re.compile(r"\[(asy)(.*?)\]"))
        assert tag_and_args[0] == "asy"
        assert tag_and_args[1] == {}

    def test_args(self):
        text = r"""meow
lorem [asy meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""
        tag_and_args = get_tag_and_args(text, 11, re.compile(r"\[(asy)(.*?)\]"))
        assert tag_and_args[0] == "asy"
        assert tag_and_args[1] == {
            "meow": "hi",
            "width": "50",
            "alt": "meow neow",
            "caption": "this",
        }


class TestValidateArgs:
    def test_invalid_args(self):
        text = r"""meow
lorem [asy meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""

        with pytest.raises(ValueError) as context:
            test_args = validate_args(
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

        test_args = validate_args(
            text, 11, re.compile(r"\[(asy)(.*?)\]"), ["width", "alt", "caption"]
        )

        assert test_args is True

    def test_empty_args(self):
        text = r"""meow
lorem [asy]some random stuff
[/asy]"""

        test_args = validate_args(
            text, 11, re.compile(r"\[(asy)(.*?)\]"), ["width", "alt", "caption"]
        )

        assert test_args is False


class TestConvertToHtml:
    def test_code_without_lang(self):
        text = r"""lorem [code]some random stuff[/code] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(code)(.*?)\]"), re.compile(r"\[/code\]")
        )

        assert res == (
            r"""<pre>
<code class="language-plaintext">
some random stuff
</code>
</pre>"""
        )

    def test_code_with_lang(self):
        text = r"""lorem [code lang=html]some random stuff[/code] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(code)(.*?)\]"), re.compile(r"\[/code\]")
        )
        assert res == (
            r"""<pre>
<code class="language-html">
some random stuff
</code>
</pre>"""
        )

    def test_color_without_hex(self):
        text = r"""lorem [color]some random stuff[/color] lorem"""
        with pytest.raises(ValueError) as context:
            res = convert_to_html(
                text,
                6,
                re.compile(r"\[(color)(.*?)\]"),
                re.compile(r"\[/color\]"),
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_color_with_hex(self):
        text = r"""lorem [color hex=#FFFFFF]some random stuff[/color] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(color)(.*?)\]"),
            re.compile(r"\[/color\]"),
        )
        assert (
            res == r"""<span style="color: #FFFFFF;">some random stuff</span>"""
        )

    def test_img_without_args(self):
        text = r"""lorem [img]some random stuff[/img] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(img)(.*?)\]"),
            re.compile(r"\[/img\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="some random stuff">
</figure>"""
        )

    def test_img_with_width_and_alt(self):
        text = r"""lorem [img width=50 alt="meow hi"]some random stuff[/img] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(img)(.*?)\]"),
            re.compile(r"\[/img\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="some random stuff" alt="meow hi" style="width: 50%; height: auto;">
</figure>"""
        )

    def test_img_with_caption(self):
        text = r"""lorem [img caption="some caption"]some random stuff[/img] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(img)(.*?)\]"),
            re.compile(r"\[/img\]"),
        )
        assert (
            res
            == r"""<figure>
<img src="some random stuff">
<figcaption>some caption</figcaption>
</figure>"""
        )

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

    def test_quote(self):
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
