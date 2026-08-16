import re

import pytest

from bloops.bloopser import convert_to_html, get_tag_and_args, validate_args

# TODO: maybe add even more tests? idk


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


class TestConvertToHtml:
    def test_simple_tag_conversion(self):
        text = r"""lorem [b]some random stuff[/b] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(b)\]"), re.compile(r"\[/b\]")
        )
        assert res == (r"""<strong>some random stuff</strong>""")

    def test_proof(self):
        text = r"""lorem [proof]some random stuff[/proof] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(proof)\]"), re.compile(r"\[/proof\]")
        )
        assert res == (
            r"""<div>
<i>Proof.</i> some random stuff<span class="qed">&#9632;</span>
</div>"""
        )

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
            _ = convert_to_html(
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
        text = r"""lorem [quote]some random stuff[/quote] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(quote)(.*?)\]"),
            re.compile(r"\[/quote\]"),
        )
        assert (
            res
            == r"""<blockquote>
<p>some random stuff</p>
</blockquote>"""
        )

    def test_quote_with_citation(self):
        text = r"""lorem [quote link=https://www.bubudroid.me]some random stuff[/quote] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(quote)(.*?)\]"),
            re.compile(r"\[/quote\]"),
        )
        assert (
            res
            == r"""<blockquote cite="https://www.bubudroid.me">
<p>some random stuff</p>
</blockquote>"""
        )

    def test_quote_with_author(self):
        text = r"""lorem [quote author="bubu droid"]some random stuff[/quote] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(quote)(.*?)\]"),
            re.compile(r"\[/quote\]"),
        )
        assert (
            res
            == r"""<figure>
<blockquote>
<p>some random stuff</p>
</blockquote>
<figcaption>
<cite>bubu droid</cite>
</figcaption>
</figure>"""
        )

    def test_url_without_link(self):
        text = r"""lorem [url]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = convert_to_html(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                re.compile(r"\[/url\]"),
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_url_with_invalid_target(self):
        text = r"""lorem [url link=https://www.bubudroid.me target=meow]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = convert_to_html(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                re.compile(r"\[/url\]"),
            )
        assert context.type is ValueError
        assert "Invalid target value provided" in str(context.value)

    def test_url_without_target(self):
        text = r"""lorem [url link=https://www.bubudroid.me]some random stuff[/url] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(url)(.*?)\]"),
            re.compile(r"\[/url\]"),
        )
        assert (
            res
            == r"""<a href="https://www.bubudroid.me">some random stuff</a>"""
        )

    def test_url_with_target(self):
        text = r"""lorem [url link=https://www.bubudroid.me target=blank]some random stuff[/url] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(url)(.*?)\]"),
            re.compile(r"\[/url\]"),
        )
        assert (
            res
            == r"""<a href="https://www.bubudroid.me" target="_blank">some random stuff</a>"""
        )

    def test_math_box_thm(self):
        text = r"""lorem [theorem]some random stuff[/theorem] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(theorem)(.*?)\]"),
            re.compile(r"\[/theorem\]"),
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Theorem.</span>
some random stuff
</div>"""
        )

    def test_math_box_prop(self):
        text = r"""lorem [proposition]some random stuff[/proposition] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(proposition)(.*?)\]"),
            re.compile(r"\[/proposition\]"),
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Proposition.</span>
some random stuff
</div>"""
        )

    def test_claim_box_with_desc(self):
        text = r"""lorem [claim desc="this is a claim"]some random stuff[/claim] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(claim)(.*?)\]"),
            re.compile(r"\[/claim\]"),
        )
        assert (
            res
            == r"""<div class="boxclaim">
<span class="title-inline">Claim (this is a claim) —</span>
some random stuff
</div>"""
        )
