import pathlib

import pytest

from bloops.validator import generate_asy_diags


class TestGenerateAsyDiags:
    def test_clear_cache_files(self) -> None:
        for path in [
            pathlib.Path("./build/meow-1.asy"),
            pathlib.Path("./build/meow-2.asy"),
            pathlib.Path("./build/meow-1.svg"),
            pathlib.Path("./build/cache.json"),
        ]:
            if path.exists():
                path.unlink()

    def test_correct_asy(self) -> None:
        generate_asy_diags(
            {"meow-1": 6},
            correct_asy,
            pathlib.Path("./"),
            pathlib.Path("./build/"),
        )

    def test_incorrect_asy(self) -> None:
        with pytest.raises(ValueError) as context:
            generate_asy_diags(
                {"meow-2": 6},
                incorrect_asy,
                pathlib.Path("./"),
                pathlib.Path("./build/"),
            )
        assert context.type is ValueError
        assert "30.1: syntax error" in str(context.value)


correct_asy = r"""lorem
[asy src=./build/meow-1.svg label=meow-1]
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
[/asy] lorem"""

incorrect_asy = r"""lorem
[asy src=./build/meow-2.svg label=meow-2]
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
dot("$S$", S, NE)
dot("$U$", T, NW);
clip((-1,-0.3)--(1,-0.3)--(1,1.2)--(-1,1.2)--cycle);
[/asy] lorem"""
