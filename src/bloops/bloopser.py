import re

from bloops._helper import get_tag_and_args
from bloops.bracer import get_close_delim_end_index, gobble_inside_delim
from bloops.vars import BBCODE_TAGS


def convert_bbcode_to_html(
    text: str,
    bbcode_tags: list[
        tuple[re.Pattern[str], re.Pattern[str], list[str]]
    ] = BBCODE_TAGS,
) -> str:
    for tag_tuple in bbcode_tags:
        open_delim = tag_tuple[0]
        close_delim = tag_tuple[1]
        index = 0
        match = open_delim.search(text, index)
        while match:
            index = match.start()
            text = (
                text[:index]
                + _convert_tag_to_html(text, index, open_delim, close_delim)
                + text[
                    get_close_delim_end_index(
                        text, index, open_delim, close_delim
                    )
                    + 1 :
                ]
            )
            match = open_delim.search(text, index + 1)

    # TODO: shift the avatar to integration server and use the static link
    return f"""<!doctype html>
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
      MathJax = {{
        tex: {{
          inlineMath: {{"[+]": [['$', '$']]}}
        }},
        svg: {{
          fontCache: 'global'
        }},
        output: {{
          displayOverflow: "linebreak",
          linebreaks: {{
            inline: true,
            width: "100%",
            lineleading: 0.2,
            LinebreakVisitor: null,
          }},
        }},
      }};
    </script>
    <script
      defer
      src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js"
    ></script>
  </head>
  <body>
    {text}
  </body>
</html>"""


def _convert_tag_to_html(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
) -> str:
    tag_and_args = get_tag_and_args(text, open_delim_start_index, open_delim)
    tag, args = tag_and_args

    content: list[str] = []
    optional_args_list: list[str] = []
    inner_content = gobble_inside_delim(
        text, open_delim_start_index, open_delim, close_delim
    ).strip()

    if tag in ["asy", "code", "color", "img", "list", "quote", "url"]:
        if tag == "asy":
            asy_dict = args
            content.append("<figure>")
            if "alt" in asy_dict:
                optional_args_list.append(f'alt="{asy_dict["alt"]}"')
            if "width" in asy_dict:
                optional_args_list.append(
                    f'style="width: {asy_dict["width"]}%; height: auto;"'
                )
            content.append(
                f'<img src="{asy_dict["src"]}" {" ".join(optional_args_list)}>'
                if optional_args_list
                else f'<img src="{asy_dict["src"]}">'
            )
            if "caption" in asy_dict:
                content.append(
                    f"<figcaption>{asy_dict['caption']}</figcaption>"
                )
            content.append("</figure>")

        elif tag == "code":
            content.append("<pre>")
            code_dict = args
            if "lang" not in code_dict:
                content.append('<code class="language-plaintext">')
            else:
                content.append(f'<code class="language-{code_dict["lang"]}">')
            content.append(inner_content)
            content.append("</code>")
            content.append("</pre>")

        elif tag == "color":
            color_dict = args
            content.append(
                f'<span style="color: {color_dict["hex"]};">'
                + inner_content
                + "</span>"
            )

        elif tag == "img":
            img_dict = args
            content.append("<figure>")
            if "alt" in img_dict:
                optional_args_list.append(f'alt="{img_dict["alt"]}"')
            if "width" in img_dict:
                optional_args_list.append(
                    f'style="width: {img_dict["width"]}%; height: auto;"'
                )
            content.append(
                f'<img src="{img_dict["src"]}" {" ".join(optional_args_list)}>'
                if optional_args_list
                else f'<img src="{img_dict["src"]}">'
            )
            if "caption" in img_dict:
                content.append(
                    f"<figcaption>{img_dict['caption']}</figcaption>"
                )
            content.append("</figure>")

        elif tag == "list":
            list_dict = args
            if "type" in list_dict and list_dict["type"] == "ol":
                if "style" not in list_dict:
                    content.append("<ol>")
                else:
                    content.append(f'<ol type="{list_dict["style"]}">')
                content.append(inner_content)
                content.append("</ol>")
            else:
                if "style" not in list_dict:
                    content.append("<ul>")
                else:
                    content.append(
                        f'<ul style="list-style-type: {list_dict["style"]};">'
                    )
                content.append(inner_content)
                content.append("</ul>")

        elif tag == "quote":
            quote_dict = args
            if "author" in quote_dict:
                content.append("<figure>")
            if "link" in quote_dict:
                content.append(f'<blockquote cite="{quote_dict["link"]}">')
            else:
                content.append("<blockquote>")
            content.append(f"<p>{inner_content}</p>")
            content.append("</blockquote>")
            if "author" in quote_dict:
                content.append("<figcaption>")
                content.append(f"<cite>{quote_dict['author']}</cite>")
                content.append("</figcaption>")
                content.append("</figure>")

        elif tag == "url":
            url_dict = args
            if "target" in url_dict:
                content.append(
                    f'<a href="{url_dict["link"]}" target="_{url_dict["target"]}">{inner_content}</a>'
                )
            else:
                content.append(
                    f'<a href="{url_dict["link"]}" target="_blank">{inner_content}</a>'
                )

    if tag in [
        "theorem",
        "lemma",
        "proposition",
        "corollary",
        "example",
        "claim",
        "problem",
        "exercise",
    ]:
        if tag in ["theorem", "lemma"]:
            content.append('<div class="boxtheorem">')
        elif tag in ["proposition", "corollary"]:
            content.append('<div class="boxproposition">')
        elif tag in ["example"]:
            content.append('<div class="boxexample">')
        elif tag in ["claim"]:
            content.append('<div class="boxclaim">')
        elif tag in ["problem", "exercise"]:
            content.append('<div class="boxproblem">')
        if "title" in args:
            if tag not in ["claim", "problem", "exercise"]:
                content.append(
                    f'<span class="title-block">{tag.title()} ({args["title"]}).</span>'
                )
            elif tag == "claim":
                content.append(
                    f'<span class="title-inline">{tag.title()} ({args["title"]}) —</span>'
                )
            else:
                content.append(
                    f'<span class="title-inline">{tag.title()} ({args["title"]}).</span>'
                )
        else:
            if tag not in ["claim", "problem", "exercise"]:
                content.append(
                    f'<span class="title-block">{tag.title()}.</span>'
                )
            elif tag == "claim":
                content.append(
                    f'<span class="title-inline">{tag.title()} —</span>'
                )
            else:
                content.append(
                    f'<span class="title-inline">{tag.title()}.</span>'
                )
        content.append(inner_content)
        content.append("</div>")

    if tag in [
        "b",
        "i",
        "u",
        "s",
        "*",
        "sub",
        "sup",
        "proof",
        "soln",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    ]:
        inline_code_dict = {
            "b": "strong",
            "i": "em",
            "u": "u",
            "s": "s",
            "*": "li",
            "sub": "sub",
            "sup": "sup",
            "h1": "h1",
            "h2": "h2",
            "h3": "h3",
            "h4": "h4",
            "h5": "h5",
            "h6": "h6",
        }

        if tag == "proof":
            content.append("<div>")
            content.append(
                f'<i class="proof">Proof.</i>\n{inner_content}<span class="qed">&#9633;</span>'
            )
            content.append("</div>")
        elif tag == "soln":
            content.append("<div>")
            content.append(
                f'<i class="proof">Solution.</i>\n{inner_content}<span class="qed">&#9632;</span>'
            )
            content.append("</div>")
        else:
            content.append(
                f"<{inline_code_dict[tag]}>{inner_content}</{inline_code_dict[tag]}>"
            )

    return "\n".join(content)
