from bloops.bloopser import transpile_all_tags


class TestTranspileAll:
    def test_correct_code(self) -> None:
        text = r"""[h1]This is The Main Heading of This Page[/h1]
[h2]2nd heading[/h2]
[h3]3rd heading[/h3]
[h4]4th heading[/h4]
[h5]5th heading[/h5]
[h6]6th heading[/h6]

[h2]this is some[h3]h3 inside h2[/h3][/h2]

This is an asy diagram with some caption text.

[asy src=static/meow.svg label=meow width=50 caption="some caption text"]
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

This is some dummy python code.
[code lang=python]
from bloops import bigfatW
print("hello")
[/code]

Some [color hex=#4B0082]fancy colored text[/color].

$$
  \measuredangle ABC=\measuredangle DEF=
  \measuredangle GHI=\measuredangle JKL=
  \measuredangle MNO=\measuredangle PQR=
  \measuredangle STU=\measuredangle VWX
$$

Here is an image with caption.
[img src=static/test-img.jpg width=10 alt=meow caption="yet some other caption"][/img]

[list type=ul style=square]
[*]item one[/*]
[*]item two[/*]
[*]item three[/*]
[/list]

[quote author="sun tzu" link="www.google.com"]
in order to confuse the enemy, you must confuse yourself first.
[/quote]

Here is a link: [url link="https://www.bubudroid.me" target=self]this is some link[/url].

Here are some math blocks with titles.

[theorem title=meow]
some theorem statement.
[/theorem]

[lemma title=meow]
some theorem statement.
[/lemma]

[proposition title=meow]
some theorem statement.
[/proposition]

[corollary title=meow]
some theorem statement.
[/corollary]

[example title=meow]
some theorem statement.
[/example]

[claim title=meow]
some theorem statement.
[/claim]

[problem title=meow]
some theorem statement.
[/problem]

[exercise title=meow]
some theorem statement.
[/exercise]

Here are some math blocks without titles.

[theorem]
some theorem statement.
[/theorem]

[lemma]
some theorem statement.
[/lemma]

[proposition]
some theorem statement.
[/proposition]

[corollary]
some theorem statement.
[/corollary]

[example]
some theorem statement.
[/example]

[claim]
some theorem statement.
[/claim]

[problem]
some theorem statement.
[/problem]

[exercise]
some theorem statement.
[/exercise]

[soln]
this is a solution.
[/soln]

[proof]
and this is a proof.
[/proof]

Now some text formattings.

[b][i]bold and italic[/i][/b] with some [s]strikethrough[/s]
and [u]underline[/u] to top it off. [sup]14[/sup]P[sub]3[/sub]."""

        output_text = r"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bloops Preview</title>
    <link
      rel="icon"
      type="image/x-icon"
      href="https://avatar.artofproblemsolving.com/avatar_778606.png"
    />
    <link rel="stylesheet" href="static/style.css" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.12.0/styles/tokyo-night-dark.min.css"
    />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.12.0/highlight.min.js"></script>
    <script>
      hljs.highlightAll();
    </script>
    <script>
      MathJax = {
        tex: {
          inlineMath: {"[+]": [['$', '$']]}
        },
        svg: {
          fontCache: 'global'
        },
        output: {
          displayOverflow: "linebreak",
          linebreaks: {
            inline: true,
            width: "100%",
            lineleading: 0.2,
            LinebreakVisitor: null,
          },
        },
      };
    </script>
    <script
      defer
      src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js"
    ></script>
  </head>
  <body>
    <h1>This is The Main Heading of This Page</h1>
<h2>2nd heading</h2>
<h3>3rd heading</h3>
<h4>4th heading</h4>
<h5>5th heading</h5>
<h6>6th heading</h6>

<h2>this is some<h3>h3 inside h2</h3></h2>

This is an asy diagram with some caption text.

<figure>
<img src="static/meow.svg" style="width: 50%; height: auto;">
<figcaption>some caption text</figcaption>
</figure>

This is some dummy python code.
<pre>
<code class="language-python">
from bloops import bigfatW
print("hello")
</code>
</pre>

Some <span style="color: #4B0082;">fancy colored text</span>.

$$
  \measuredangle ABC=\measuredangle DEF=
  \measuredangle GHI=\measuredangle JKL=
  \measuredangle MNO=\measuredangle PQR=
  \measuredangle STU=\measuredangle VWX
$$

Here is an image with caption.
<figure>
<img src="static/test-img.jpg" alt="meow" style="width: 10%; height: auto;">
<figcaption>yet some other caption</figcaption>
</figure>

<ul style="list-style-type: square;">
<li>item one</li>
<li>item two</li>
<li>item three</li>
</ul>

<figure>
<blockquote cite="www.google.com">
<p>in order to confuse the enemy, you must confuse yourself first.</p>
</blockquote>
<figcaption>
<cite>sun tzu</cite>
</figcaption>
</figure>

Here is a link: <a href="https://www.bubudroid.me" target="_self">this is some link</a>.

Here are some math blocks with titles.

<div class="boxtheorem">
<span class="title-block">Theorem (meow).</span>
some theorem statement.
</div>

<div class="boxtheorem">
<span class="title-block">Lemma (meow).</span>
some theorem statement.
</div>

<div class="boxproposition">
<span class="title-block">Proposition (meow).</span>
some theorem statement.
</div>

<div class="boxproposition">
<span class="title-block">Corollary (meow).</span>
some theorem statement.
</div>

<div class="boxexample">
<span class="title-block">Example (meow).</span>
some theorem statement.
</div>

<div class="boxclaim">
<span class="title-inline">Claim (meow) —</span>
some theorem statement.
</div>

<div class="boxproblem">
<span class="title-inline">Problem (meow).</span>
some theorem statement.
</div>

<div class="boxproblem">
<span class="title-inline">Exercise (meow).</span>
some theorem statement.
</div>

Here are some math blocks without titles.

<div class="boxtheorem">
<span class="title-block">Theorem.</span>
some theorem statement.
</div>

<div class="boxtheorem">
<span class="title-block">Lemma.</span>
some theorem statement.
</div>

<div class="boxproposition">
<span class="title-block">Proposition.</span>
some theorem statement.
</div>

<div class="boxproposition">
<span class="title-block">Corollary.</span>
some theorem statement.
</div>

<div class="boxexample">
<span class="title-block">Example.</span>
some theorem statement.
</div>

<div class="boxclaim">
<span class="title-inline">Claim —</span>
some theorem statement.
</div>

<div class="boxproblem">
<span class="title-inline">Problem.</span>
some theorem statement.
</div>

<div class="boxproblem">
<span class="title-inline">Exercise.</span>
some theorem statement.
</div>

<div>
<i class="proof">Solution.</i>
this is a solution.<span class="qed">&#9633;</span>
</div>

<div>
<i class="proof">Proof.</i>
and this is a proof.<span class="qed">&#9632;</span>
</div>

Now some text formattings.

<strong><em>bold and italic</em></strong> with some <s>strikethrough</s>
and <u>underline</u> to top it off. <sup>14</sup>P<sub>3</sub>.
  </body>
</html>"""
        res = transpile_all_tags(text)
        assert res == output_text
