from bloops.bloopser import _convert_tag_to_html
from bloops.vars import BBCODE_TAGS


class TestMathBoxesWithoutDesc:
    def test_theorem_box(self) -> None:
        text = r"""lorem [theorem]some random stuff[/theorem] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["theorem"][0],
            BBCODE_TAGS["theorem"][1],
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Theorem.</span>
some random stuff
</div>"""
        )

    def test_lemma_box(self) -> None:
        text = r"""lorem [lemma]some random stuff[/lemma] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["lemma"][0],
            BBCODE_TAGS["lemma"][1],
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Lemma.</span>
some random stuff
</div>"""
        )

    def test_prop_box(self) -> None:
        text = r"""lorem [proposition]some random stuff[/proposition] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["proposition"][0],
            BBCODE_TAGS["proposition"][1],
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Proposition.</span>
some random stuff
</div>"""
        )

    def test_corollary_box(self) -> None:
        text = r"""lorem [corollary]some random stuff[/corollary] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["corollary"][0],
            BBCODE_TAGS["corollary"][1],
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Corollary.</span>
some random stuff
</div>"""
        )

    def test_example_box(self) -> None:
        text = r"""lorem [example]some random stuff[/example] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["example"][0],
            BBCODE_TAGS["example"][1],
        )
        assert (
            res
            == r"""<div class="boxexample">
<span class="title-block">Example.</span>
some random stuff
</div>"""
        )

    def test_claim_box(self) -> None:
        text = r"""lorem [claim]some random stuff[/claim] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["claim"][0],
            BBCODE_TAGS["claim"][1],
        )
        assert (
            res
            == r"""<div class="boxclaim">
<span class="title-inline">Claim —</span>
some random stuff
</div>"""
        )

    def test_problem_box(self) -> None:
        text = r"""lorem [problem]some random stuff[/problem] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["problem"][0],
            BBCODE_TAGS["problem"][1],
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Problem.</span>
some random stuff
</div>"""
        )

    def test_exercise_box(self) -> None:
        text = r"""lorem [exercise]some random stuff[/exercise] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["exercise"][0],
            BBCODE_TAGS["exercise"][1],
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Exercise.</span>
some random stuff
</div>"""
        )


class TestMathBoxesWithDesc:
    def test_theorem_box(self) -> None:
        text = r"""lorem [theorem title="some description"]some random stuff[/theorem] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["theorem"][0],
            BBCODE_TAGS["theorem"][1],
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Theorem (some description).</span>
some random stuff
</div>"""
        )

    def test_lemma_box(self) -> None:
        text = r"""lorem [lemma title="some description"]some random stuff[/lemma] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["lemma"][0],
            BBCODE_TAGS["lemma"][1],
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Lemma (some description).</span>
some random stuff
</div>"""
        )

    def test_prop_box(self) -> None:
        text = r"""lorem [proposition title="some description"]some random stuff[/proposition] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["proposition"][0],
            BBCODE_TAGS["proposition"][1],
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Proposition (some description).</span>
some random stuff
</div>"""
        )

    def test_corollary_box(self) -> None:
        text = r"""lorem [corollary title="some description"]some random stuff[/corollary] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["corollary"][0],
            BBCODE_TAGS["corollary"][1],
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Corollary (some description).</span>
some random stuff
</div>"""
        )

    def test_example_box(self) -> None:
        text = r"""lorem [example title="some description"]some random stuff[/example] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["example"][0],
            BBCODE_TAGS["example"][1],
        )
        assert (
            res
            == r"""<div class="boxexample">
<span class="title-block">Example (some description).</span>
some random stuff
</div>"""
        )

    def test_claim_box(self) -> None:
        text = r"""lorem [claim title="some description"]some random stuff[/claim] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["claim"][0],
            BBCODE_TAGS["claim"][1],
        )
        assert (
            res
            == r"""<div class="boxclaim">
<span class="title-inline">Claim (some description) —</span>
some random stuff
</div>"""
        )

    def test_problem_box(self) -> None:
        text = r"""lorem [problem title="some description"]some random stuff[/problem] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["problem"][0],
            BBCODE_TAGS["problem"][1],
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Problem (some description).</span>
some random stuff
</div>"""
        )

    def test_exercise_box(self) -> None:
        text = r"""lorem [exercise title="some description"]some random stuff[/exercise] lorem"""
        res = _convert_tag_to_html(
            text,
            6,
            BBCODE_TAGS["exercise"][0],
            BBCODE_TAGS["exercise"][1],
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Exercise (some description).</span>
some random stuff
</div>"""
        )
