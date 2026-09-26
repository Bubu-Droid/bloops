import re

# TODO: handle the case when there is a ] inside the string
# TODO: maybe convert this into a dict to not hardcode re.Pattern(s)
# in tests
BBCODE_TAGS: list[tuple[re.Pattern[str], re.Pattern[str], list[str]]] = [
    (
        re.compile(r"\[(asy)(.*?)\]"),
        re.compile(r"\[/asy\]"),
        ["src", "label", "width", "alt", "caption"],
    ),
    (re.compile(r"\[(code)(.*?)\]"), re.compile(r"\[/code\]"), ["lang"]),
    (re.compile(r"\[(color)(.*?)\]"), re.compile(r"\[/color\]"), ["hex"]),
    (
        re.compile(r"\[(img)(.*?)\]"),
        re.compile(r"\[/img\]"),
        ["src", "width", "alt", "caption"],
    ),
    (
        re.compile(r"\[(list)(.*?)\]"),
        re.compile(r"\[/list\]"),
        ["type", "style"],
    ),
    (
        re.compile(r"\[(quote)(.*?)\]"),
        re.compile(r"\[/quote\]"),
        ["author", "link"],
    ),
    (
        re.compile(r"\[(url)(.*?)\]"),
        re.compile(r"\[/url\]"),
        ["link", "target"],
    ),
    (re.compile(r"\[(theorem)(.*?)\]"), re.compile(r"\[/theorem\]"), ["title"]),
    (re.compile(r"\[(lemma)(.*?)\]"), re.compile(r"\[/lemma\]"), ["title"]),
    (
        re.compile(r"\[(proposition)(.*?)\]"),
        re.compile(r"\[/proposition\]"),
        ["title"],
    ),
    (
        re.compile(r"\[(corollary)(.*?)\]"),
        re.compile(r"\[/corollary\]"),
        ["title"],
    ),
    (re.compile(r"\[(example)(.*?)\]"), re.compile(r"\[/example\]"), ["title"]),
    (re.compile(r"\[(claim)(.*?)\]"), re.compile(r"\[/claim\]"), ["title"]),
    (re.compile(r"\[(problem)(.*?)\]"), re.compile(r"\[/problem\]"), ["title"]),
    (
        re.compile(r"\[(exercise)(.*?)\]"),
        re.compile(r"\[/exercise\]"),
        ["title"],
    ),
    (re.compile(r"\[(b)\]"), re.compile(r"\[/b\]"), []),
    (re.compile(r"\[(i)\]"), re.compile(r"\[/i\]"), []),
    (re.compile(r"\[(u)\]"), re.compile(r"\[/u\]"), []),
    (re.compile(r"\[(s)\]"), re.compile(r"\[/s\]"), []),
    (re.compile(r"\[(\*)\]"), re.compile(r"\[/\*\]"), []),
    (re.compile(r"\[(sub)\]"), re.compile(r"\[/sub\]"), []),
    (re.compile(r"\[(sup)\]"), re.compile(r"\[/sup\]"), []),
    (re.compile(r"\[(proof)\]"), re.compile(r"\[/proof\]"), []),
    (re.compile(r"\[(soln)\]"), re.compile(r"\[/soln\]"), []),
    (re.compile(r"\[(h1)\]"), re.compile(r"\[/h1\]"), []),
    (re.compile(r"\[(h2)\]"), re.compile(r"\[/h2\]"), []),
    (re.compile(r"\[(h3)\]"), re.compile(r"\[/h3\]"), []),
    (re.compile(r"\[(h4)\]"), re.compile(r"\[/h4\]"), []),
    (re.compile(r"\[(h5)\]"), re.compile(r"\[/h5\]"), []),
    (re.compile(r"\[(h6)\]"), re.compile(r"\[/h6\]"), []),
]

STYLESHEET = r""":root {
  /* base */
  --tn-bg: #1a1b26;
  --tn-bg-raised: #1e2030;
  --tn-border: #2a2e42;
  --tn-border-soft: #22253a;

  /* text */
  --tn-fg: #c0caf5;
  --tn-fg-dim: #7a82ac;
  --tn-fg-faint: #565f89;

  /* accents */
  --tn-blue: #7aa2f7;
  --tn-cyan: #7dcfff;
  --tn-green: #9ece6a;
  --tn-magenta: #bb9af7;
  --tn-orange: #ff9e64;
  --tn-red: #f7768e;
  --tn-yellow: #e0af68;

  /* fonts */
  --lora: "Lora", serif;
  --open-sans: "Open Sans", sans-serif;
  --jetbrains-mono: "JetBrains Mono", monospace;
}

* {
  box-sizing: border-box;
}

html {
  background: var(--tn-bg);
}

body {
  margin: 0;
  padding: 5rem 1.5rem 8rem;
  background: var(--tn-bg);
  color: var(--tn-fg);
  font-family: var(--open-sans);
  font-optical-sizing: auto;
  font-size: 1.125rem;
  line-height: 1.75;
  max-width: 660px;
  margin-inline: auto;
  /* stylelint-disable-next-line value-keyword-case */
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: var(--lora);
  font-weight: normal;
  line-height: initial;
}

h1 {
  font-style: italic;
}

/* ---------------- text formatting ---------------- */

strong {
  color: var(--tn-fg);
  font-weight: 600;
}

em {
  font-style: italic;
}

s {
  color: var(--tn-fg-faint);
  text-decoration-color: var(--tn-red);
}

u {
  text-decoration-color: var(--tn-cyan);
  text-underline-offset: 3px;
}

sup,
sub {
  font-family: var(--jetbrains-mono);
  font-size: 0.7em;
  color: var(--tn-fg-dim);
}

p {
  margin: 1.4em 0;
}

/* ---------------- links ---------------- */

a {
  color: var(--tn-blue);
  text-decoration: none;
  border-bottom: 1px solid #7aa2f759;
  transition:
    border-color 0.15s ease,
    color 0.15s ease;
}

a:hover {
  color: var(--tn-cyan);
  border-bottom-color: var(--tn-cyan);
}

/* ---------------- lists ---------------- */

ul,
ol {
  padding-left: 1.4em;
  margin: 1.4em 0;
}

li {
  margin: 0.4em 0;
}

li::marker {
  color: var(--tn-magenta);
}

/* ---------------- figures & images ---------------- */

figure {
  margin: 2.5rem 0;
  text-align: center;
}

figure img {
  display: block;
  margin: 0 auto;
  border-radius: 3px;
}

figcaption {
  margin-top: 0.75rem;
  font-family: var(--lora);
  font-style: italic;
  font-size: 1rem;
  color: var(--tn-fg-dim);
}

figcaption cite {
  font-style: italic;
  color: var(--tn-orange);
}

/* ---------------- blockquote ---------------- */

blockquote {
  margin: 0;
  padding: 0;
  color: var(--tn-fg);
  font-family: var(--lora);
  font-style: italic;
}

blockquote p {
  margin: 0.6em 0;
}

figure:has(blockquote) {
  text-align: left;
  margin: 2.5rem 0;
  padding: 0.3em 1.3em;
  border-left: 2px solid var(--tn-yellow);
}

figure:has(blockquote) figcaption {
  margin-top: 0.4em;
  text-align: right;
}

/* ---------------- code ---------------- */

pre {
  background: var(--tn-bg-raised);
  border: 1px solid var(--tn-border);
  border-radius: 6px;
  overflow-x: auto;
  line-height: initial;
}

code {
  font-family: var(--jetbrains-mono);
}

pre code.hljs {
  background: transparent;
  padding: 0 1em !important;
}

/* ---------------- theorem-style boxes ---------------- */

[class^="box"] {
  margin: 2rem 0;
  padding: 0.75rem 1.3rem;
  background: var(--tn-bg-raised);
  border-left: 3px solid var(--tn-fg-faint);
  border-radius: 0 4px 4px 0;
  font-size: 1.05rem;
}

[class^="box"] p {
  margin: 0.8em 0 0;
}

[class^="box"] .title-block {
  display: block;
  margin-bottom: 0.5em;
  font-weight: 600;
  font-family: var(--lora);
  font-style: italic;
}

[class^="box"] .title-inline {
  font-weight: 600;
  margin-right: 0.35em;
  font-family: var(--lora);
  font-style: italic;
}

.boxtheorem {
  border-left-color: var(--tn-blue);
}

.boxtheorem .title-block,
.boxtheorem .title-inline {
  color: var(--tn-blue);
}

.boxproposition {
  border-left-color: var(--tn-cyan);
}

.boxproposition .title-block,
.boxproposition .title-inline {
  color: var(--tn-cyan);
}

.boxexample {
  background: transparent;
  border: 1px solid var(--tn-green);
  border-radius: 0;
}

.boxexample .title-block,
.boxexample .title-inline {
  color: var(--tn-green);
}

.boxclaim {
  border-left-color: var(--tn-magenta);
}

.boxclaim .title-block,
.boxclaim .title-inline {
  color: var(--tn-magenta);
}

.boxproblem {
  border-left-color: var(--tn-orange);
}

.boxproblem .title-block,
.boxproblem .title-inline {
  color: var(--tn-orange);
}

/* proof / solution */
div:has(> .proof) {
  margin: 1.8rem 0;
  padding-left: 0.1rem;
}

.proof {
  font-family: var(--lora);
  font-style: italic;
  color: var(--tn-fg-dim);
}

.qed {
  float: right;
  font-size: 0.8em;
  margin-top: 0.2em;
  color: var(--tn-fg-faint);
}

/* ---------------- misc ---------------- */

::selection {
  background: #7aa2f740;
  color: var(--tn-fg);
}

@media (width <= 480px) {
  body {
    padding: 3rem 1.1rem 6rem;
    font-size: 1.05rem;
  }
}"""

# TODO: shift the avatar to integration server and use the static link
ERROR_TEMPLATE = r"""<!doctype html>
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
    <style>
      .error-msg {
        display: flex;
        flex-direction: column;
        text-align: center;
        margin-bottom: 1.5em;
      }

      html,
      body {
        height: 100%;
      }

      body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }

      svg {
        width: 35%;
        min-width: 300px;
        min-height: 300px;
      }

      #qr-bg {
        fill: var(--tn-fg);
      }

      #qr-fg {
        fill: var(--tn-bg);
      }
    </style>
  </head>
  <body>
    <h1 class="error-msg">
      <span>An error has occurred.</span>
      <span>Check the terminal logs.</span>
    </h1>
    <svg
      width="328"
      height="328"
      viewBox="0 0 328 328"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:ev="http://www.w3.org/2001/xml-events"
    >
      <rect x="0" y="0" width="328" height="328" fill="#ffffff" />
      <defs>
        <rect id="p" width="8" height="8" />
      </defs>
      <g fill="#000000">
        <use xlink:href="#p" x="32" y="32" />
        <use xlink:href="#p" x="32" y="40" />
        <use xlink:href="#p" x="32" y="48" />
        <use xlink:href="#p" x="32" y="56" />
        <use xlink:href="#p" x="32" y="64" />
        <use xlink:href="#p" x="32" y="72" />
        <use xlink:href="#p" x="32" y="80" />
        <use xlink:href="#p" x="32" y="96" />
        <use xlink:href="#p" x="32" y="104" />
        <use xlink:href="#p" x="32" y="112" />
        <use xlink:href="#p" x="32" y="120" />
        <use xlink:href="#p" x="32" y="136" />
        <use xlink:href="#p" x="32" y="144" />
        <use xlink:href="#p" x="32" y="152" />
        <use xlink:href="#p" x="32" y="160" />
        <use xlink:href="#p" x="32" y="192" />
        <use xlink:href="#p" x="32" y="208" />
        <use xlink:href="#p" x="32" y="216" />
        <use xlink:href="#p" x="32" y="240" />
        <use xlink:href="#p" x="32" y="248" />
        <use xlink:href="#p" x="32" y="256" />
        <use xlink:href="#p" x="32" y="264" />
        <use xlink:href="#p" x="32" y="272" />
        <use xlink:href="#p" x="32" y="280" />
        <use xlink:href="#p" x="32" y="288" />
        <use xlink:href="#p" x="40" y="32" />
        <use xlink:href="#p" x="40" y="80" />
        <use xlink:href="#p" x="40" y="96" />
        <use xlink:href="#p" x="40" y="120" />
        <use xlink:href="#p" x="40" y="152" />
        <use xlink:href="#p" x="40" y="160" />
        <use xlink:href="#p" x="40" y="168" />
        <use xlink:href="#p" x="40" y="192" />
        <use xlink:href="#p" x="40" y="208" />
        <use xlink:href="#p" x="40" y="224" />
        <use xlink:href="#p" x="40" y="240" />
        <use xlink:href="#p" x="40" y="288" />
        <use xlink:href="#p" x="48" y="32" />
        <use xlink:href="#p" x="48" y="48" />
        <use xlink:href="#p" x="48" y="56" />
        <use xlink:href="#p" x="48" y="64" />
        <use xlink:href="#p" x="48" y="80" />
        <use xlink:href="#p" x="48" y="96" />
        <use xlink:href="#p" x="48" y="136" />
        <use xlink:href="#p" x="48" y="144" />
        <use xlink:href="#p" x="48" y="184" />
        <use xlink:href="#p" x="48" y="200" />
        <use xlink:href="#p" x="48" y="224" />
        <use xlink:href="#p" x="48" y="240" />
        <use xlink:href="#p" x="48" y="256" />
        <use xlink:href="#p" x="48" y="264" />
        <use xlink:href="#p" x="48" y="272" />
        <use xlink:href="#p" x="48" y="288" />
        <use xlink:href="#p" x="56" y="32" />
        <use xlink:href="#p" x="56" y="48" />
        <use xlink:href="#p" x="56" y="56" />
        <use xlink:href="#p" x="56" y="64" />
        <use xlink:href="#p" x="56" y="80" />
        <use xlink:href="#p" x="56" y="96" />
        <use xlink:href="#p" x="56" y="104" />
        <use xlink:href="#p" x="56" y="112" />
        <use xlink:href="#p" x="56" y="144" />
        <use xlink:href="#p" x="56" y="152" />
        <use xlink:href="#p" x="56" y="160" />
        <use xlink:href="#p" x="56" y="176" />
        <use xlink:href="#p" x="56" y="184" />
        <use xlink:href="#p" x="56" y="192" />
        <use xlink:href="#p" x="56" y="216" />
        <use xlink:href="#p" x="56" y="224" />
        <use xlink:href="#p" x="56" y="240" />
        <use xlink:href="#p" x="56" y="256" />
        <use xlink:href="#p" x="56" y="264" />
        <use xlink:href="#p" x="56" y="272" />
        <use xlink:href="#p" x="56" y="288" />
        <use xlink:href="#p" x="64" y="32" />
        <use xlink:href="#p" x="64" y="48" />
        <use xlink:href="#p" x="64" y="56" />
        <use xlink:href="#p" x="64" y="64" />
        <use xlink:href="#p" x="64" y="80" />
        <use xlink:href="#p" x="64" y="120" />
        <use xlink:href="#p" x="64" y="128" />
        <use xlink:href="#p" x="64" y="136" />
        <use xlink:href="#p" x="64" y="168" />
        <use xlink:href="#p" x="64" y="176" />
        <use xlink:href="#p" x="64" y="184" />
        <use xlink:href="#p" x="64" y="192" />
        <use xlink:href="#p" x="64" y="216" />
        <use xlink:href="#p" x="64" y="224" />
        <use xlink:href="#p" x="64" y="240" />
        <use xlink:href="#p" x="64" y="256" />
        <use xlink:href="#p" x="64" y="264" />
        <use xlink:href="#p" x="64" y="272" />
        <use xlink:href="#p" x="64" y="288" />
        <use xlink:href="#p" x="72" y="32" />
        <use xlink:href="#p" x="72" y="80" />
        <use xlink:href="#p" x="72" y="104" />
        <use xlink:href="#p" x="72" y="112" />
        <use xlink:href="#p" x="72" y="136" />
        <use xlink:href="#p" x="72" y="152" />
        <use xlink:href="#p" x="72" y="160" />
        <use xlink:href="#p" x="72" y="168" />
        <use xlink:href="#p" x="72" y="200" />
        <use xlink:href="#p" x="72" y="240" />
        <use xlink:href="#p" x="72" y="288" />
        <use xlink:href="#p" x="80" y="32" />
        <use xlink:href="#p" x="80" y="40" />
        <use xlink:href="#p" x="80" y="48" />
        <use xlink:href="#p" x="80" y="56" />
        <use xlink:href="#p" x="80" y="64" />
        <use xlink:href="#p" x="80" y="72" />
        <use xlink:href="#p" x="80" y="80" />
        <use xlink:href="#p" x="80" y="96" />
        <use xlink:href="#p" x="80" y="112" />
        <use xlink:href="#p" x="80" y="128" />
        <use xlink:href="#p" x="80" y="144" />
        <use xlink:href="#p" x="80" y="160" />
        <use xlink:href="#p" x="80" y="176" />
        <use xlink:href="#p" x="80" y="192" />
        <use xlink:href="#p" x="80" y="208" />
        <use xlink:href="#p" x="80" y="224" />
        <use xlink:href="#p" x="80" y="240" />
        <use xlink:href="#p" x="80" y="248" />
        <use xlink:href="#p" x="80" y="256" />
        <use xlink:href="#p" x="80" y="264" />
        <use xlink:href="#p" x="80" y="272" />
        <use xlink:href="#p" x="80" y="280" />
        <use xlink:href="#p" x="80" y="288" />
        <use xlink:href="#p" x="88" y="112" />
        <use xlink:href="#p" x="88" y="128" />
        <use xlink:href="#p" x="88" y="144" />
        <use xlink:href="#p" x="88" y="168" />
        <use xlink:href="#p" x="88" y="176" />
        <use xlink:href="#p" x="88" y="192" />
        <use xlink:href="#p" x="96" y="32" />
        <use xlink:href="#p" x="96" y="48" />
        <use xlink:href="#p" x="96" y="56" />
        <use xlink:href="#p" x="96" y="64" />
        <use xlink:href="#p" x="96" y="80" />
        <use xlink:href="#p" x="96" y="96" />
        <use xlink:href="#p" x="96" y="104" />
        <use xlink:href="#p" x="96" y="112" />
        <use xlink:href="#p" x="96" y="120" />
        <use xlink:href="#p" x="96" y="136" />
        <use xlink:href="#p" x="96" y="152" />
        <use xlink:href="#p" x="96" y="168" />
        <use xlink:href="#p" x="96" y="176" />
        <use xlink:href="#p" x="96" y="184" />
        <use xlink:href="#p" x="96" y="192" />
        <use xlink:href="#p" x="96" y="232" />
        <use xlink:href="#p" x="96" y="264" />
        <use xlink:href="#p" x="96" y="272" />
        <use xlink:href="#p" x="96" y="280" />
        <use xlink:href="#p" x="96" y="288" />
        <use xlink:href="#p" x="104" y="32" />
        <use xlink:href="#p" x="104" y="56" />
        <use xlink:href="#p" x="104" y="64" />
        <use xlink:href="#p" x="104" y="72" />
        <use xlink:href="#p" x="104" y="88" />
        <use xlink:href="#p" x="104" y="104" />
        <use xlink:href="#p" x="104" y="128" />
        <use xlink:href="#p" x="104" y="152" />
        <use xlink:href="#p" x="104" y="160" />
        <use xlink:href="#p" x="104" y="168" />
        <use xlink:href="#p" x="104" y="176" />
        <use xlink:href="#p" x="104" y="184" />
        <use xlink:href="#p" x="104" y="192" />
        <use xlink:href="#p" x="104" y="200" />
        <use xlink:href="#p" x="104" y="216" />
        <use xlink:href="#p" x="104" y="264" />
        <use xlink:href="#p" x="104" y="288" />
        <use xlink:href="#p" x="112" y="64" />
        <use xlink:href="#p" x="112" y="80" />
        <use xlink:href="#p" x="112" y="136" />
        <use xlink:href="#p" x="112" y="144" />
        <use xlink:href="#p" x="112" y="168" />
        <use xlink:href="#p" x="112" y="184" />
        <use xlink:href="#p" x="112" y="200" />
        <use xlink:href="#p" x="112" y="208" />
        <use xlink:href="#p" x="112" y="224" />
        <use xlink:href="#p" x="112" y="256" />
        <use xlink:href="#p" x="112" y="264" />
        <use xlink:href="#p" x="112" y="272" />
        <use xlink:href="#p" x="112" y="288" />
        <use xlink:href="#p" x="120" y="48" />
        <use xlink:href="#p" x="120" y="56" />
        <use xlink:href="#p" x="120" y="64" />
        <use xlink:href="#p" x="120" y="88" />
        <use xlink:href="#p" x="120" y="96" />
        <use xlink:href="#p" x="120" y="104" />
        <use xlink:href="#p" x="120" y="112" />
        <use xlink:href="#p" x="120" y="120" />
        <use xlink:href="#p" x="120" y="128" />
        <use xlink:href="#p" x="120" y="152" />
        <use xlink:href="#p" x="120" y="168" />
        <use xlink:href="#p" x="120" y="184" />
        <use xlink:href="#p" x="120" y="200" />
        <use xlink:href="#p" x="120" y="208" />
        <use xlink:href="#p" x="120" y="216" />
        <use xlink:href="#p" x="120" y="224" />
        <use xlink:href="#p" x="120" y="256" />
        <use xlink:href="#p" x="120" y="264" />
        <use xlink:href="#p" x="120" y="280" />
        <use xlink:href="#p" x="128" y="48" />
        <use xlink:href="#p" x="128" y="56" />
        <use xlink:href="#p" x="128" y="80" />
        <use xlink:href="#p" x="128" y="104" />
        <use xlink:href="#p" x="128" y="160" />
        <use xlink:href="#p" x="128" y="176" />
        <use xlink:href="#p" x="128" y="200" />
        <use xlink:href="#p" x="128" y="208" />
        <use xlink:href="#p" x="128" y="216" />
        <use xlink:href="#p" x="128" y="256" />
        <use xlink:href="#p" x="128" y="264" />
        <use xlink:href="#p" x="128" y="280" />
        <use xlink:href="#p" x="136" y="40" />
        <use xlink:href="#p" x="136" y="48" />
        <use xlink:href="#p" x="136" y="56" />
        <use xlink:href="#p" x="136" y="64" />
        <use xlink:href="#p" x="136" y="72" />
        <use xlink:href="#p" x="136" y="120" />
        <use xlink:href="#p" x="136" y="128" />
        <use xlink:href="#p" x="136" y="144" />
        <use xlink:href="#p" x="136" y="160" />
        <use xlink:href="#p" x="136" y="168" />
        <use xlink:href="#p" x="136" y="208" />
        <use xlink:href="#p" x="136" y="216" />
        <use xlink:href="#p" x="136" y="224" />
        <use xlink:href="#p" x="136" y="240" />
        <use xlink:href="#p" x="136" y="256" />
        <use xlink:href="#p" x="144" y="32" />
        <use xlink:href="#p" x="144" y="48" />
        <use xlink:href="#p" x="144" y="56" />
        <use xlink:href="#p" x="144" y="64" />
        <use xlink:href="#p" x="144" y="80" />
        <use xlink:href="#p" x="144" y="96" />
        <use xlink:href="#p" x="144" y="104" />
        <use xlink:href="#p" x="144" y="128" />
        <use xlink:href="#p" x="144" y="144" />
        <use xlink:href="#p" x="144" y="176" />
        <use xlink:href="#p" x="144" y="192" />
        <use xlink:href="#p" x="144" y="200" />
        <use xlink:href="#p" x="144" y="208" />
        <use xlink:href="#p" x="144" y="232" />
        <use xlink:href="#p" x="144" y="264" />
        <use xlink:href="#p" x="144" y="288" />
        <use xlink:href="#p" x="152" y="56" />
        <use xlink:href="#p" x="152" y="64" />
        <use xlink:href="#p" x="152" y="120" />
        <use xlink:href="#p" x="152" y="136" />
        <use xlink:href="#p" x="152" y="160" />
        <use xlink:href="#p" x="152" y="168" />
        <use xlink:href="#p" x="152" y="176" />
        <use xlink:href="#p" x="152" y="224" />
        <use xlink:href="#p" x="152" y="232" />
        <use xlink:href="#p" x="152" y="248" />
        <use xlink:href="#p" x="152" y="256" />
        <use xlink:href="#p" x="152" y="264" />
        <use xlink:href="#p" x="152" y="272" />
        <use xlink:href="#p" x="160" y="32" />
        <use xlink:href="#p" x="160" y="56" />
        <use xlink:href="#p" x="160" y="64" />
        <use xlink:href="#p" x="160" y="72" />
        <use xlink:href="#p" x="160" y="80" />
        <use xlink:href="#p" x="160" y="96" />
        <use xlink:href="#p" x="160" y="136" />
        <use xlink:href="#p" x="160" y="152" />
        <use xlink:href="#p" x="160" y="192" />
        <use xlink:href="#p" x="160" y="208" />
        <use xlink:href="#p" x="160" y="232" />
        <use xlink:href="#p" x="160" y="248" />
        <use xlink:href="#p" x="160" y="288" />
        <use xlink:href="#p" x="168" y="56" />
        <use xlink:href="#p" x="168" y="72" />
        <use xlink:href="#p" x="168" y="88" />
        <use xlink:href="#p" x="168" y="96" />
        <use xlink:href="#p" x="168" y="104" />
        <use xlink:href="#p" x="168" y="112" />
        <use xlink:href="#p" x="168" y="128" />
        <use xlink:href="#p" x="168" y="168" />
        <use xlink:href="#p" x="168" y="176" />
        <use xlink:href="#p" x="168" y="184" />
        <use xlink:href="#p" x="168" y="192" />
        <use xlink:href="#p" x="168" y="224" />
        <use xlink:href="#p" x="168" y="232" />
        <use xlink:href="#p" x="168" y="280" />
        <use xlink:href="#p" x="168" y="288" />
        <use xlink:href="#p" x="176" y="32" />
        <use xlink:href="#p" x="176" y="40" />
        <use xlink:href="#p" x="176" y="72" />
        <use xlink:href="#p" x="176" y="80" />
        <use xlink:href="#p" x="176" y="88" />
        <use xlink:href="#p" x="176" y="96" />
        <use xlink:href="#p" x="176" y="104" />
        <use xlink:href="#p" x="176" y="112" />
        <use xlink:href="#p" x="176" y="144" />
        <use xlink:href="#p" x="176" y="152" />
        <use xlink:href="#p" x="176" y="160" />
        <use xlink:href="#p" x="176" y="184" />
        <use xlink:href="#p" x="176" y="192" />
        <use xlink:href="#p" x="176" y="208" />
        <use xlink:href="#p" x="176" y="216" />
        <use xlink:href="#p" x="176" y="240" />
        <use xlink:href="#p" x="176" y="256" />
        <use xlink:href="#p" x="184" y="32" />
        <use xlink:href="#p" x="184" y="48" />
        <use xlink:href="#p" x="184" y="64" />
        <use xlink:href="#p" x="184" y="72" />
        <use xlink:href="#p" x="184" y="88" />
        <use xlink:href="#p" x="184" y="96" />
        <use xlink:href="#p" x="184" y="104" />
        <use xlink:href="#p" x="184" y="128" />
        <use xlink:href="#p" x="184" y="136" />
        <use xlink:href="#p" x="184" y="144" />
        <use xlink:href="#p" x="184" y="184" />
        <use xlink:href="#p" x="184" y="200" />
        <use xlink:href="#p" x="184" y="216" />
        <use xlink:href="#p" x="184" y="232" />
        <use xlink:href="#p" x="184" y="240" />
        <use xlink:href="#p" x="184" y="280" />
        <use xlink:href="#p" x="184" y="288" />
        <use xlink:href="#p" x="192" y="32" />
        <use xlink:href="#p" x="192" y="40" />
        <use xlink:href="#p" x="192" y="64" />
        <use xlink:href="#p" x="192" y="80" />
        <use xlink:href="#p" x="192" y="88" />
        <use xlink:href="#p" x="192" y="96" />
        <use xlink:href="#p" x="192" y="104" />
        <use xlink:href="#p" x="192" y="120" />
        <use xlink:href="#p" x="192" y="160" />
        <use xlink:href="#p" x="192" y="176" />
        <use xlink:href="#p" x="192" y="200" />
        <use xlink:href="#p" x="192" y="208" />
        <use xlink:href="#p" x="192" y="224" />
        <use xlink:href="#p" x="192" y="240" />
        <use xlink:href="#p" x="192" y="248" />
        <use xlink:href="#p" x="192" y="256" />
        <use xlink:href="#p" x="192" y="264" />
        <use xlink:href="#p" x="192" y="280" />
        <use xlink:href="#p" x="192" y="288" />
        <use xlink:href="#p" x="200" y="32" />
        <use xlink:href="#p" x="200" y="72" />
        <use xlink:href="#p" x="200" y="96" />
        <use xlink:href="#p" x="200" y="152" />
        <use xlink:href="#p" x="200" y="160" />
        <use xlink:href="#p" x="200" y="168" />
        <use xlink:href="#p" x="200" y="176" />
        <use xlink:href="#p" x="200" y="192" />
        <use xlink:href="#p" x="200" y="200" />
        <use xlink:href="#p" x="200" y="240" />
        <use xlink:href="#p" x="200" y="248" />
        <use xlink:href="#p" x="200" y="256" />
        <use xlink:href="#p" x="200" y="272" />
        <use xlink:href="#p" x="200" y="288" />
        <use xlink:href="#p" x="208" y="48" />
        <use xlink:href="#p" x="208" y="56" />
        <use xlink:href="#p" x="208" y="80" />
        <use xlink:href="#p" x="208" y="88" />
        <use xlink:href="#p" x="208" y="128" />
        <use xlink:href="#p" x="208" y="136" />
        <use xlink:href="#p" x="208" y="160" />
        <use xlink:href="#p" x="208" y="168" />
        <use xlink:href="#p" x="208" y="200" />
        <use xlink:href="#p" x="208" y="208" />
        <use xlink:href="#p" x="208" y="224" />
        <use xlink:href="#p" x="208" y="240" />
        <use xlink:href="#p" x="208" y="264" />
        <use xlink:href="#p" x="216" y="32" />
        <use xlink:href="#p" x="216" y="40" />
        <use xlink:href="#p" x="216" y="88" />
        <use xlink:href="#p" x="216" y="96" />
        <use xlink:href="#p" x="216" y="104" />
        <use xlink:href="#p" x="216" y="112" />
        <use xlink:href="#p" x="216" y="160" />
        <use xlink:href="#p" x="216" y="168" />
        <use xlink:href="#p" x="216" y="184" />
        <use xlink:href="#p" x="216" y="200" />
        <use xlink:href="#p" x="216" y="208" />
        <use xlink:href="#p" x="216" y="232" />
        <use xlink:href="#p" x="216" y="240" />
        <use xlink:href="#p" x="216" y="248" />
        <use xlink:href="#p" x="216" y="256" />
        <use xlink:href="#p" x="216" y="288" />
        <use xlink:href="#p" x="224" y="32" />
        <use xlink:href="#p" x="224" y="40" />
        <use xlink:href="#p" x="224" y="48" />
        <use xlink:href="#p" x="224" y="56" />
        <use xlink:href="#p" x="224" y="64" />
        <use xlink:href="#p" x="224" y="80" />
        <use xlink:href="#p" x="224" y="120" />
        <use xlink:href="#p" x="224" y="136" />
        <use xlink:href="#p" x="224" y="152" />
        <use xlink:href="#p" x="224" y="176" />
        <use xlink:href="#p" x="224" y="184" />
        <use xlink:href="#p" x="224" y="208" />
        <use xlink:href="#p" x="224" y="216" />
        <use xlink:href="#p" x="224" y="224" />
        <use xlink:href="#p" x="224" y="232" />
        <use xlink:href="#p" x="224" y="240" />
        <use xlink:href="#p" x="224" y="248" />
        <use xlink:href="#p" x="224" y="256" />
        <use xlink:href="#p" x="224" y="264" />
        <use xlink:href="#p" x="224" y="272" />
        <use xlink:href="#p" x="224" y="280" />
        <use xlink:href="#p" x="232" y="96" />
        <use xlink:href="#p" x="232" y="120" />
        <use xlink:href="#p" x="232" y="128" />
        <use xlink:href="#p" x="232" y="136" />
        <use xlink:href="#p" x="232" y="144" />
        <use xlink:href="#p" x="232" y="152" />
        <use xlink:href="#p" x="232" y="160" />
        <use xlink:href="#p" x="232" y="176" />
        <use xlink:href="#p" x="232" y="224" />
        <use xlink:href="#p" x="232" y="256" />
        <use xlink:href="#p" x="232" y="272" />
        <use xlink:href="#p" x="232" y="288" />
        <use xlink:href="#p" x="240" y="32" />
        <use xlink:href="#p" x="240" y="40" />
        <use xlink:href="#p" x="240" y="48" />
        <use xlink:href="#p" x="240" y="56" />
        <use xlink:href="#p" x="240" y="64" />
        <use xlink:href="#p" x="240" y="72" />
        <use xlink:href="#p" x="240" y="80" />
        <use xlink:href="#p" x="240" y="104" />
        <use xlink:href="#p" x="240" y="112" />
        <use xlink:href="#p" x="240" y="152" />
        <use xlink:href="#p" x="240" y="160" />
        <use xlink:href="#p" x="240" y="168" />
        <use xlink:href="#p" x="240" y="184" />
        <use xlink:href="#p" x="240" y="200" />
        <use xlink:href="#p" x="240" y="208" />
        <use xlink:href="#p" x="240" y="224" />
        <use xlink:href="#p" x="240" y="240" />
        <use xlink:href="#p" x="240" y="256" />
        <use xlink:href="#p" x="240" y="272" />
        <use xlink:href="#p" x="240" y="280" />
        <use xlink:href="#p" x="240" y="288" />
        <use xlink:href="#p" x="248" y="32" />
        <use xlink:href="#p" x="248" y="80" />
        <use xlink:href="#p" x="248" y="104" />
        <use xlink:href="#p" x="248" y="112" />
        <use xlink:href="#p" x="248" y="120" />
        <use xlink:href="#p" x="248" y="136" />
        <use xlink:href="#p" x="248" y="144" />
        <use xlink:href="#p" x="248" y="168" />
        <use xlink:href="#p" x="248" y="192" />
        <use xlink:href="#p" x="248" y="224" />
        <use xlink:href="#p" x="248" y="256" />
        <use xlink:href="#p" x="248" y="272" />
        <use xlink:href="#p" x="248" y="288" />
        <use xlink:href="#p" x="256" y="32" />
        <use xlink:href="#p" x="256" y="48" />
        <use xlink:href="#p" x="256" y="56" />
        <use xlink:href="#p" x="256" y="64" />
        <use xlink:href="#p" x="256" y="80" />
        <use xlink:href="#p" x="256" y="96" />
        <use xlink:href="#p" x="256" y="120" />
        <use xlink:href="#p" x="256" y="128" />
        <use xlink:href="#p" x="256" y="152" />
        <use xlink:href="#p" x="256" y="160" />
        <use xlink:href="#p" x="256" y="168" />
        <use xlink:href="#p" x="256" y="184" />
        <use xlink:href="#p" x="256" y="216" />
        <use xlink:href="#p" x="256" y="224" />
        <use xlink:href="#p" x="256" y="232" />
        <use xlink:href="#p" x="256" y="240" />
        <use xlink:href="#p" x="256" y="248" />
        <use xlink:href="#p" x="256" y="256" />
        <use xlink:href="#p" x="256" y="288" />
        <use xlink:href="#p" x="264" y="32" />
        <use xlink:href="#p" x="264" y="48" />
        <use xlink:href="#p" x="264" y="56" />
        <use xlink:href="#p" x="264" y="64" />
        <use xlink:href="#p" x="264" y="80" />
        <use xlink:href="#p" x="264" y="96" />
        <use xlink:href="#p" x="264" y="112" />
        <use xlink:href="#p" x="264" y="120" />
        <use xlink:href="#p" x="264" y="136" />
        <use xlink:href="#p" x="264" y="144" />
        <use xlink:href="#p" x="264" y="152" />
        <use xlink:href="#p" x="264" y="168" />
        <use xlink:href="#p" x="264" y="200" />
        <use xlink:href="#p" x="264" y="216" />
        <use xlink:href="#p" x="264" y="256" />
        <use xlink:href="#p" x="264" y="264" />
        <use xlink:href="#p" x="264" y="272" />
        <use xlink:href="#p" x="264" y="288" />
        <use xlink:href="#p" x="272" y="32" />
        <use xlink:href="#p" x="272" y="48" />
        <use xlink:href="#p" x="272" y="56" />
        <use xlink:href="#p" x="272" y="64" />
        <use xlink:href="#p" x="272" y="80" />
        <use xlink:href="#p" x="272" y="96" />
        <use xlink:href="#p" x="272" y="152" />
        <use xlink:href="#p" x="272" y="160" />
        <use xlink:href="#p" x="272" y="192" />
        <use xlink:href="#p" x="272" y="200" />
        <use xlink:href="#p" x="272" y="232" />
        <use xlink:href="#p" x="272" y="240" />
        <use xlink:href="#p" x="272" y="248" />
        <use xlink:href="#p" x="272" y="256" />
        <use xlink:href="#p" x="272" y="288" />
        <use xlink:href="#p" x="280" y="32" />
        <use xlink:href="#p" x="280" y="80" />
        <use xlink:href="#p" x="280" y="112" />
        <use xlink:href="#p" x="280" y="120" />
        <use xlink:href="#p" x="280" y="144" />
        <use xlink:href="#p" x="280" y="152" />
        <use xlink:href="#p" x="280" y="176" />
        <use xlink:href="#p" x="280" y="192" />
        <use xlink:href="#p" x="280" y="208" />
        <use xlink:href="#p" x="280" y="224" />
        <use xlink:href="#p" x="280" y="232" />
        <use xlink:href="#p" x="280" y="264" />
        <use xlink:href="#p" x="280" y="272" />
        <use xlink:href="#p" x="288" y="32" />
        <use xlink:href="#p" x="288" y="40" />
        <use xlink:href="#p" x="288" y="48" />
        <use xlink:href="#p" x="288" y="56" />
        <use xlink:href="#p" x="288" y="64" />
        <use xlink:href="#p" x="288" y="72" />
        <use xlink:href="#p" x="288" y="80" />
        <use xlink:href="#p" x="288" y="96" />
        <use xlink:href="#p" x="288" y="104" />
        <use xlink:href="#p" x="288" y="112" />
        <use xlink:href="#p" x="288" y="168" />
        <use xlink:href="#p" x="288" y="184" />
        <use xlink:href="#p" x="288" y="192" />
        <use xlink:href="#p" x="288" y="200" />
        <use xlink:href="#p" x="288" y="208" />
        <use xlink:href="#p" x="288" y="216" />
        <use xlink:href="#p" x="288" y="248" />
        <use xlink:href="#p" x="288" y="280" />
      </g>
      <g></g>
    </svg>
  </body>
</html>"""
