import re

from bloops.bracer import (
    get_error_line,
    gobble_inside_delim,
)


def convert_to_html(
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
    )

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
            if inner_content:
                content.append(f"<figcaption>{inner_content}</figcaption>")
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
                    f'<a href="{url_dict["link"]}">{inner_content}</a>'
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
        if "desc" in args:
            if tag not in ["claim", "problem", "exercise"]:
                content.append(
                    f'<span class="title-block">{tag.title()} ({args["desc"]}).</span>'
                )
            elif tag == "claim":
                content.append(
                    f'<span class="title-inline">{tag.title()} ({args["desc"]}) —</span>'
                )
            else:
                content.append(
                    f'<span class="title-inline">{tag.title()} ({args["desc"]}).</span>'
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

    if tag in ["b", "i", "u", "s", "*", "sub", "sup", "proof", "soln"]:
        inline_code_dict = {
            "b": "strong",
            "i": "em",
            "u": "u",
            "s": "s",
            "*": "li",
            "sub": "sub",
            "sup": "sup",
        }

        if tag == "proof":
            content.append("<div>")
            content.append(
                f'<i>Proof.</i> {inner_content}<span class="qed">&#9632;</span>'
            )
            content.append("</div>")
        elif tag == "soln":
            content.append("<div>")
            content.append(
                f'<i>Solution.</i> {inner_content}<span class="qed">&#9633;</span>'
            )
            content.append("</div>")
        else:
            content.append(
                f"<{inline_code_dict[tag]}>{inner_content}</{inline_code_dict[tag]}>"
            )

    return "\n".join(content)


def get_tag_and_args(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
) -> tuple[str, dict[str, str]]:
    match = open_delim.match(text, open_delim_start_index)
    if not match:
        error_line = get_error_line(text, open_delim_start_index)
        raise SyntaxError(
            "No opening delimiter at the current position."
            + "\n\n"
            + f"{error_line[0]}: {error_line[1]}"
        )

    pattern = r'[\w]+=".*?"|[\w]+=[^\s]+'
    if len(match.groups()) <= 1:
        return (match.group(1), {})

    args_list: list[str] = re.findall(pattern, match.group(2))
    args_dict = {
        arg.split("=")[0]: (arg.split("=")[1]).strip('"') for arg in args_list
    }

    return (match.group(1), args_dict)
