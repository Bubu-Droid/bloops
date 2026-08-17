import re

from bloops.bloopser import convert_to_html


class TestMathBoxesWithoutDesc:
    def test_theorem_box(self):
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

    def test_lemma_box(self):
        text = r"""lorem [lemma]some random stuff[/lemma] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(lemma)(.*?)\]"),
            re.compile(r"\[/lemma\]"),
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Lemma.</span>
some random stuff
</div>"""
        )

    def test_prop_box(self):
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

    def test_corollary_box(self):
        text = r"""lorem [corollary]some random stuff[/corollary] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(corollary)(.*?)\]"),
            re.compile(r"\[/corollary\]"),
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Corollary.</span>
some random stuff
</div>"""
        )

    def test_example_box(self):
        text = r"""lorem [example]some random stuff[/example] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(example)(.*?)\]"),
            re.compile(r"\[/example\]"),
        )
        assert (
            res
            == r"""<div class="boxexample">
<span class="title-block">Example.</span>
some random stuff
</div>"""
        )

    def test_claim_box(self):
        text = r"""lorem [claim]some random stuff[/claim] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(claim)(.*?)\]"),
            re.compile(r"\[/claim\]"),
        )
        assert (
            res
            == r"""<div class="boxclaim">
<span class="title-inline">Claim —</span>
some random stuff
</div>"""
        )

    def test_problem_box(self):
        text = r"""lorem [problem]some random stuff[/problem] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(problem)(.*?)\]"),
            re.compile(r"\[/problem\]"),
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Problem.</span>
some random stuff
</div>"""
        )

    def test_exercise_box(self):
        text = r"""lorem [exercise]some random stuff[/exercise] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(exercise)(.*?)\]"),
            re.compile(r"\[/exercise\]"),
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Exercise.</span>
some random stuff
</div>"""
        )


class TestMathBoxesWithDesc:
    def test_theorem_box(self):
        text = r"""lorem [theorem desc="some description"]some random stuff[/theorem] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(theorem)(.*?)\]"),
            re.compile(r"\[/theorem\]"),
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Theorem (some description).</span>
some random stuff
</div>"""
        )

    def test_lemma_box(self):
        text = r"""lorem [lemma desc="some description"]some random stuff[/lemma] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(lemma)(.*?)\]"),
            re.compile(r"\[/lemma\]"),
        )
        assert (
            res
            == r"""<div class="boxtheorem">
<span class="title-block">Lemma (some description).</span>
some random stuff
</div>"""
        )

    def test_prop_box(self):
        text = r"""lorem [proposition desc="some description"]some random stuff[/proposition] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(proposition)(.*?)\]"),
            re.compile(r"\[/proposition\]"),
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Proposition (some description).</span>
some random stuff
</div>"""
        )

    def test_corollary_box(self):
        text = r"""lorem [corollary desc="some description"]some random stuff[/corollary] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(corollary)(.*?)\]"),
            re.compile(r"\[/corollary\]"),
        )
        assert (
            res
            == r"""<div class="boxproposition">
<span class="title-block">Corollary (some description).</span>
some random stuff
</div>"""
        )

    def test_example_box(self):
        text = r"""lorem [example desc="some description"]some random stuff[/example] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(example)(.*?)\]"),
            re.compile(r"\[/example\]"),
        )
        assert (
            res
            == r"""<div class="boxexample">
<span class="title-block">Example (some description).</span>
some random stuff
</div>"""
        )

    def test_claim_box(self):
        text = r"""lorem [claim desc="some description"]some random stuff[/claim] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(claim)(.*?)\]"),
            re.compile(r"\[/claim\]"),
        )
        assert (
            res
            == r"""<div class="boxclaim">
<span class="title-inline">Claim (some description) —</span>
some random stuff
</div>"""
        )

    def test_problem_box(self):
        text = r"""lorem [problem desc="some description"]some random stuff[/problem] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(problem)(.*?)\]"),
            re.compile(r"\[/problem\]"),
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Problem (some description).</span>
some random stuff
</div>"""
        )

    def test_exercise_box(self):
        text = r"""lorem [exercise desc="some description"]some random stuff[/exercise] lorem"""
        res = convert_to_html(
            text,
            6,
            re.compile(r"\[(exercise)(.*?)\]"),
            re.compile(r"\[/exercise\]"),
        )
        assert (
            res
            == r"""<div class="boxproblem">
<span class="title-inline">Exercise (some description).</span>
some random stuff
</div>"""
        )
