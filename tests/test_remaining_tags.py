import re

from bloops.bloopser import convert_to_html


class TestCodeTag:
    def test_code_without_lang(self) -> None:
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

    def test_code_with_lang(self) -> None:
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


class TestColorTag:
    def test_color_with_hex(self) -> None:
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


class TestQuote:
    def test_quote(self) -> None:
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

    def test_quote_with_citation(self) -> None:
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

    def test_quote_with_author(self) -> None:
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

    def test_quote_with_cite_and_author(self) -> None:
        text = r"""lorem [quote link=https://www.bubudroid.me author="bubu droid"]some random stuff[/quote] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(quote)(.*?)\]"),
            re.compile(r"\[/quote\]"),
        )
        assert (
            res
            == r"""<figure>
<blockquote cite="https://www.bubudroid.me">
<p>some random stuff</p>
</blockquote>
<figcaption>
<cite>bubu droid</cite>
</figcaption>
</figure>"""
        )


class TestUrlTag:
    def test_url_without_target(self) -> None:
        text = r"""lorem [url link=https://www.bubudroid.me]some random stuff[/url] lorem"""
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

    def test_url_with_target(self) -> None:
        text = r"""lorem [url link=https://www.bubudroid.me target=self]some random stuff[/url] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(url)(.*?)\]"),
            re.compile(r"\[/url\]"),
        )
        assert (
            res
            == r"""<a href="https://www.bubudroid.me" target="_self">some random stuff</a>"""
        )
