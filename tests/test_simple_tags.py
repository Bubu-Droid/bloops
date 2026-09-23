import re

from bloops.bloopser import convert_to_html


class TestSimpleTag:
    def test_b_tag(self) -> None:
        text = r"""lorem [b]some random stuff[/b] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(b)\]"), re.compile(r"\[/b\]")
        )
        # assert res == (r"""<strong>some random stuff</strong>""")
        assert res == (r"""<strong>ome random stuff</strong>""")

    def test_i_tag(self) -> None:
        text = r"""lorem [i]some random stuff[/i] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(i)\]"), re.compile(r"\[/i\]")
        )
        assert res == (r"""<em>some random stuff</em>""")

    def test_u_tag(self) -> None:
        text = r"""lorem [u]some random stuff[/u] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(u)\]"), re.compile(r"\[/u\]")
        )
        assert res == (r"""<u>some random stuff</u>""")

    def test_s_tag(self) -> None:
        text = r"""lorem [s]some random stuff[/s] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(s)\]"), re.compile(r"\[/s\]")
        )
        assert res == (r"""<s>some random stuff</s>""")

    def test_li_tag(self) -> None:
        text = r"""lorem [*]some random stuff[/*] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(\*)\]"), re.compile(r"\[/\*\]")
        )
        assert res == (r"""<li>some random stuff</li>""")

    def test_sub_tag(self) -> None:
        text = r"""lorem [sub]some random stuff[/sub] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(sub)\]"), re.compile(r"\[/sub\]")
        )
        assert res == (r"""<sub>some random stuff</sub>""")

    def test_sup_tag(self) -> None:
        text = r"""lorem [sup]some random stuff[/sup] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(sup)\]"), re.compile(r"\[/sup\]")
        )
        assert res == (r"""<sup>some random stuff</sup>""")

    def test_proof(self) -> None:
        text = r"""lorem [proof]some random stuff[/proof] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(proof)\]"), re.compile(r"\[/proof\]")
        )
        assert res == (
            r"""<div>
<i class="proof">Proof.</i>
some random stuff<span class="qed">&#9633;</span>
</div>"""
        )

    def test_soln(self) -> None:
        text = r"""lorem [soln]some random stuff[/soln] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(soln)\]"), re.compile(r"\[/soln\]")
        )
        assert res == (
            r"""<div>
<i class="proof">Solution.</i>
some random stuff<span class="qed">&#9632;</span>
</div>"""
        )

    def test_h1(self) -> None:
        text = r"""lorem [h1]a[/h1] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h1)\]"), re.compile(r"\[/h1\]")
        )
        assert res == (r"""<h1>a</h1>""")

    def test_h2(self) -> None:
        text = r"""lorem [h2]a[/h2] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h2)\]"), re.compile(r"\[/h2\]")
        )
        assert res == (r"""<h2>a</h2>""")

    def test_h3(self) -> None:
        text = r"""lorem [h3]a[/h3] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h3)\]"), re.compile(r"\[/h3\]")
        )
        assert res == (r"""<h3>a</h3>""")

    def test_h4(self) -> None:
        text = r"""lorem [h4]a[/h4] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h4)\]"), re.compile(r"\[/h4\]")
        )
        assert res == (r"""<h4>a</h4>""")

    def test_h5(self) -> None:
        text = r"""lorem [h5]a[/h5] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h5)\]"), re.compile(r"\[/h5\]")
        )
        assert res == (r"""<h5>a</h5>""")

    def test_h6(self) -> None:
        text = r"""lorem [h6]a[/h6] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(h6)\]"), re.compile(r"\[/h6\]")
        )
        assert res == (r"""<h6>a</h6>""")
