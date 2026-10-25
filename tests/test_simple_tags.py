from bloops.bloopser import _convert_tag_to_html
from bloops.vars import BBCODE_TAGS


class TestSimpleTag:
    def test_b_tag(self) -> None:
        text = r"""lorem [b]some random stuff[/b] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["b"][0], BBCODE_TAGS["b"][1]
        )
        assert res == (r"""<strong>some random stuff</strong>""")

    def test_i_tag(self) -> None:
        text = r"""lorem [i]some random stuff[/i] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["i"][0], BBCODE_TAGS["i"][1]
        )
        assert res == (r"""<em>some random stuff</em>""")

    def test_u_tag(self) -> None:
        text = r"""lorem [u]some random stuff[/u] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["u"][0], BBCODE_TAGS["u"][1]
        )
        assert res == (r"""<u>some random stuff</u>""")

    def test_s_tag(self) -> None:
        text = r"""lorem [s]some random stuff[/s] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["s"][0], BBCODE_TAGS["s"][1]
        )
        assert res == (r"""<s>some random stuff</s>""")

    def test_li_tag(self) -> None:
        text = r"""lorem [*]some random stuff[/*] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["*"][0], BBCODE_TAGS["*"][1]
        )
        assert res == (r"""<li>some random stuff</li>""")

    def test_sub_tag(self) -> None:
        text = r"""lorem [sub]some random stuff[/sub] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["sub"][0], BBCODE_TAGS["sub"][1]
        )
        assert res == (r"""<sub>some random stuff</sub>""")

    def test_sup_tag(self) -> None:
        text = r"""lorem [sup]some random stuff[/sup] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["sup"][0], BBCODE_TAGS["sup"][1]
        )
        assert res == (r"""<sup>some random stuff</sup>""")

    def test_proof(self) -> None:
        text = r"""lorem [proof]some random stuff[/proof] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["proof"][0], BBCODE_TAGS["proof"][1]
        )
        assert res == (
            r"""<div>
<i class="proof">Proof.</i>
some random stuff<span class="qed">&#9633;</span>
</div>"""
        )

    def test_soln(self) -> None:
        text = r"""lorem [soln]some random stuff[/soln] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["soln"][0], BBCODE_TAGS["soln"][1]
        )
        assert res == (
            r"""<div>
<i class="proof">Solution.</i>
some random stuff<span class="qed">&#9632;</span>
</div>"""
        )

    def test_h1(self) -> None:
        text = r"""lorem [h1]a[/h1] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h1"][0], BBCODE_TAGS["h1"][1]
        )
        assert res == (r"""<h1>a</h1>""")

    def test_h2(self) -> None:
        text = r"""lorem [h2]a[/h2] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h2"][0], BBCODE_TAGS["h2"][1]
        )
        assert res == (r"""<h2>a</h2>""")

    def test_h3(self) -> None:
        text = r"""lorem [h3]a[/h3] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h3"][0], BBCODE_TAGS["h3"][1]
        )
        assert res == (r"""<h3>a</h3>""")

    def test_h4(self) -> None:
        text = r"""lorem [h4]a[/h4] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h4"][0], BBCODE_TAGS["h4"][1]
        )
        assert res == (r"""<h4>a</h4>""")

    def test_h5(self) -> None:
        text = r"""lorem [h5]a[/h5] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h5"][0], BBCODE_TAGS["h5"][1]
        )
        assert res == (r"""<h5>a</h5>""")

    def test_h6(self) -> None:
        text = r"""lorem [h6]a[/h6] lorem"""
        res = _convert_tag_to_html(
            text, 6, BBCODE_TAGS["h6"][0], BBCODE_TAGS["h6"][1]
        )
        assert res == (r"""<h6>a</h6>""")
