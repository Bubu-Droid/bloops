import re

from bloops.bloopser import convert_to_html


class TestSimpleTag:
    def test_b_tag(self):
        text = r"""lorem [b]some random stuff[/b] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(b)\]"), re.compile(r"\[/b\]")
        )
        assert res == (r"""<strong>some random stuff</strong>""")

    def test_i_tag(self):
        text = r"""lorem [i]some random stuff[/i] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(i)\]"), re.compile(r"\[/i\]")
        )
        assert res == (r"""<em>some random stuff</em>""")

    def test_u_tag(self):
        text = r"""lorem [u]some random stuff[/u] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(u)\]"), re.compile(r"\[/u\]")
        )
        assert res == (r"""<u>some random stuff</u>""")

    def test_s_tag(self):
        text = r"""lorem [s]some random stuff[/s] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(s)\]"), re.compile(r"\[/s\]")
        )
        assert res == (r"""<s>some random stuff</s>""")

    def test_li_tag(self):
        text = r"""lorem [*]some random stuff[/*] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(\*)\]"), re.compile(r"\[/\*\]")
        )
        assert res == (r"""<li>some random stuff</li>""")

    def test_sub_tag(self):
        text = r"""lorem [sub]some random stuff[/sub] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(sub)\]"), re.compile(r"\[/sub\]")
        )
        assert res == (r"""<sub>some random stuff</sub>""")

    def test_sup_tag(self):
        text = r"""lorem [sup]some random stuff[/sup] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(sup)\]"), re.compile(r"\[/sup\]")
        )
        assert res == (r"""<sup>some random stuff</sup>""")

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

    def test_soln(self):
        text = r"""lorem [soln]some random stuff[/soln] lorem"""
        res = convert_to_html(
            text, 6, re.compile(r"\[(soln)\]"), re.compile(r"\[/soln\]")
        )
        assert res == (
            r"""<div>
<i>Solution.</i> some random stuff<span class="qed">&#9633;</span>
</div>"""
        )
