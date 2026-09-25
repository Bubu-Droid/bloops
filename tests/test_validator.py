import pathlib
import re

import pytest

from bloops.validator import (
    _validate_args,
    compile_asy_diagrams,
    validate_bbcode,
)


class TestValidateArgs:
    def test_invalid_args(self) -> None:
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello meow=hi width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""

        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                11,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert "Invalid argument provided" in str(context.value)
        assert "are the only valid" in str(context.value)

    def test_valid_args(self) -> None:
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello width=50 alt="meow neow" caption=this]some random stuff
[/asy]"""
        _validate_args(
            text,
            11,
            re.compile(r"\[(asy)(.*?)\]"),
            ["src", "label", "width", "alt", "caption"],
        )

    def test_empty_args(self) -> None:
        text = r"""meow
lorem [asy src=/home/bubu/meow.png label=hello]some random stuff
[/asy]"""

        _validate_args(
            text,
            11,
            re.compile(r"\[(asy)(.*?)\]"),
            ["src", "label", "width", "alt", "caption"],
        )

    def test_asy_without_src(self) -> None:
        text = r"""lorem [asy label=hello]some random stuff[/asy] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert 'Missing mandatory parameter "src' in str(context.value)

    def test_asy_without_label(self) -> None:
        text = r"""lorem [asy src=/home/bubu/meow.png]some random stuff[/asy] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(asy)(.*?)\]"),
                ["src", "label", "width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert 'Missing mandatory parameter "label' in str(context.value)

    def test_img_without_src(self) -> None:
        text = r"""lorem [img]some random stuff[/img] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(img)(.*?)\]"),
                ["width", "alt", "caption"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_list_ul_with_invalid_style(self) -> None:
        text = (
            r"""lorem [list type=ul style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                ["type", "style"],
            )
        assert context.type is ValueError
        assert "Invalid <ul> style provided" in str(context.value)

    def test_list_ol_with_invalid_style(self) -> None:
        text = (
            r"""lorem [list type=ol style=meow]some random stuff[/list] lorem"""
        )
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(list)(.*?)\]"),
                ["type", "style"],
            )
        assert context.type is ValueError
        assert "Invalid <ol> style provided" in str(context.value)

    def test_color_without_hex(self) -> None:
        text = r"""lorem [color]some random stuff[/color] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(color)(.*?)\]"),
                ["hex"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_url_without_link(self) -> None:
        text = r"""lorem [url]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                ["link", "target"],
            )
        assert context.type is ValueError
        assert "Missing mandatory parameter" in str(context.value)

    def test_url_with_invalid_target(self) -> None:
        text = r"""lorem [url link=https://www.bubudroid.me target=meow]some random stuff[/url] lorem"""
        with pytest.raises(ValueError) as context:
            _ = _validate_args(
                text,
                6,
                re.compile(r"\[(url)(.*?)\]"),
                ["link", "target"],
            )
        assert context.type is ValueError
        assert "Invalid target value provided" in str(context.value)

    def test_incorrect_code(self) -> None:
        text = r"""asdf [asy src="static/meow.svg" label=meow]
        pair M = (0,0);
        pair B = (-1/sqrt(3),0);
        pair C = (1/sqrt(3),0);
        pair A = dir(105);
        pair P = (2B+C)/3;
        pair Q = (B+2C)/3;
        pair R = (2C+A)/3;
        pair S = (C+2A)/3;
        pair U = (2A+B)/3;
        pair T = (A+2B)/3;
        import graph;
        import geometry;
        size(11cm);
        pen dps = linewidth(0.5) + fontsize(13);
        defaultpen(dps);
        draw(circle(M, 1), linewidth(0.5) + red);
        draw(C--A, linewidth(0.5));
        draw(A--B, linewidth(0.5));
        draw(B--C, linewidth(0.5));
        draw(circumcircle(R,S,Q), linewidth(0.5) + dashed + blue);
        dot("$M$", M, NW);
        dot("$B$", B, NW);
        dot("$C$", C, NE);
        dot("$A$", A, NW);
        dot("$P$", P, NW);
        dot("$Q$", Q, NW);
        dot("$R$", R, NE);
        dot("$T$", U, NW);
        dot("$S$", S, NE);
        dot("$U$", T, NW);
        clip((-1,-0.3)--(1,-0.3)--(1,1.2)--(-1,1.2)--cycle);
        [/asy]

        this is a new line
        this is a new line
        this is another new line

        [b]

        some more random lorem text"""
        with pytest.raises(SyntaxError) as context:
            _ = compile_asy_diagrams(
                validate_bbcode(text),
                text,
                pathlib.Path("./"),
                pathlib.Path("./build/"),
            )
        assert context.type is SyntaxError
        assert "Failed to find an opening pair for delimiter." in str(
            context.value
        )
        assert "39:" in str(context.value)
        assert "[b]" in str(context.value)
