import json
import pathlib
import re
import subprocess
from typing import cast

from bloops.bracer import (
    get_error_line,
    gobble_inside_delim,
)

# FIX: gotta move the error raises to validator function
# and also check for duplicate asy filenames


def convert_to_html(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
    in_dir: pathlib.Path | None = None,
    out_dir: pathlib.Path | None = None,
) -> str:
    tag_and_args = get_tag_and_args(text, open_delim_start_index, open_delim)
    tag = tag_and_args[0]
    args = tag_and_args[1]

    content: list[str] = []
    optional_args_list: list[str] = []
    inner_content = gobble_inside_delim(
        text, open_delim_start_index, open_delim, close_delim
    )

    if tag in ["asy", "code", "color", "img", "list", "quote", "url"]:
        if tag == "asy":
            # FIX: move this entire code block to validator function
            asy_dict = args
            if "src" not in asy_dict:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Missing mandatory parameter "src."'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )
            if "label" not in asy_dict:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Missing mandatory parameter "label."'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )
            if not (in_dir and out_dir):
                raise TypeError(
                    "Input and output directory paths are mandatory arguments."
                )
            build_dir = in_dir / "build/"
            build_dir.mkdir(exist_ok=True)
            asy_cache_file = build_dir / "cache.json"
            if not asy_cache_file.exists():
                asy_cache_file.touch()
                with asy_cache_file.open("w", encoding="utf-8") as f:
                    _ = f.write("{}")
            with asy_cache_file.open("r", encoding="utf-8") as f:
                asy_cache_content = cast(dict[str, str], json.load(f))
            # if asy_dict["filename"] in asy_cache_content:
            #     error_line = get_error_line(text, open_delim_start_index)
            #     raise ValueError(
            #         'Missing mandatory parameter "A diagram with the same filename already exists."'
            #         + "\n\n"
            #         + f"{error_line[0]}: {error_line[1]}"
            #     )
            changed = False
            if asy_dict["label"] not in asy_cache_content:
                asy_cache_content[asy_dict["label"]] = inner_content
                changed = True
            else:
                if asy_cache_content[asy_dict["label"]] != inner_content:
                    asy_cache_content[asy_dict["label"]] = inner_content
                    changed = True
            asy_code_file = build_dir / f"{asy_dict['label']}.asy"

            if changed:
                with asy_code_file.open("w", encoding="utf-8") as f:
                    _ = f.write(inner_content)

                try:
                    _ = subprocess.run(
                        [
                            "asy",
                            asy_code_file.absolute(),
                            "-f",
                            "svg",
                            "-o",
                            out_dir.absolute(),
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                except subprocess.CalledProcessError as e:
                    error_line = get_error_line(text, open_delim_start_index)
                    error_message: str = cast(str, e.stderr)
                    raise ValueError(
                        f"{error_line[0]}: {error_line[1]}"
                        + "\n\n"
                        + error_message
                    )

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
            if inner_content:
                content.append(f"<figcaption>{inner_content}</figcaption>")
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


def validate_args(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    valid_args: list[str],
    in_dir: pathlib.Path | None = None,
    out_dir: pathlib.Path | None = None,
) -> bool:
    tag_and_args = get_tag_and_args(text, open_delim_start_index, open_delim)
    tag = tag_and_args[0]
    args = tag_and_args[1]

    # learning c++ has made me so pedantic that i
    # even wanna optimize this O(mn) search, son ;-;

    for arg in args:
        if arg not in valid_args:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                "Invalid argument provided."
                + f"{error_line[0]}: {error_line[1]}"
                + "\n\n"
                + f"{', '.join(valid_args)} are the only valid arguments."
            )

    if tag == "asy":
        asy_dict = args
        if "src" not in asy_dict:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Missing mandatory parameter "src."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        if "label" not in asy_dict:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Missing mandatory parameter "label."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        if not (in_dir and out_dir):
            raise TypeError(
                "Input and output directory paths are mandatory arguments."
            )
        build_dir = in_dir / "build/"
        build_dir.mkdir(exist_ok=True)
        asy_cache_file = build_dir / "cache.json"
        if not asy_cache_file.exists():
            asy_cache_file.touch()
            with asy_cache_file.open("w", encoding="utf-8") as f:
                _ = f.write("{}")
        # with asy_cache_file.open("r", encoding="utf-8") as f:
        #     asy_cache_content = cast(dict[str, str], json.load(f))
        # if asy_dict["filename"] in asy_cache_content:
        #     error_line = get_error_line(text, open_delim_start_index)
        #     raise ValueError(
        #         'Missing mandatory parameter "A diagram with the same filename already exists."'
        #         + "\n\n"
        #         + f"{error_line[0]}: {error_line[1]}"
        #     )

    elif tag == "color":
        color_dict = args
        if "hex" not in color_dict:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Missing mandatory parameter "hex."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )

    elif tag == "img":
        img_dict = args
        if "src" not in img_dict:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Missing mandatory parameter "src."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )

    elif tag == "list":
        list_dict = args
        if "type" in list_dict and list_dict["type"] not in ["ul", "ol"]:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Invalid list type provided. Valid types are "ul" and "ol" only.'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        if "type" in list_dict and list_dict["type"] == "ol":
            if "style" in list_dict and list_dict["style"] not in [
                "1",
                "A",
                "a",
                "I",
                "i",
            ]:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Invalid <ol> style provided. Valid ol styles are "1", "A", "a", "I", and "i" only.'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )
        else:
            if "style" in list_dict and list_dict["style"] not in [
                "disc",
                "circle",
                "square",
                "none",
            ]:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Invalid <ul> style provided. Valid ul styles are "disc", "circle", "square", and "none" only.'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )

    elif tag == "url":
        url_dict = args
        if "link" not in url_dict:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Missing mandatory parameter "link."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        if "target" in url_dict and url_dict["target"] not in [
            "self",
            "blank",
        ]:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                'Invalid target value provided. Target can only be "self" or "blank."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )

    return args != {}


def validate_and_setup_asy(
    text: str,
    open_delim: re.Pattern[str],
    valid_args: list[str],
    in_dir: pathlib.Path | None = None,
    out_dir: pathlib.Path | None = None,
):
    index = 0
    match = re.search(open_delim, text[index:])
    label_list: list[str] = []

    while match:
        index = match.start()
        args = get_tag_and_args(text, index, open_delim)[1]

        for arg in args:
            if arg not in valid_args:
                error_line = get_error_line(text, index)
                raise ValueError(
                    "Invalid argument provided."
                    + f"{error_line[0]}: {error_line[1]}"
                    + "\n\n"
                    + f"{', '.join(valid_args)} are the only valid arguments."
                )

        asy_dict = args
        if "src" not in asy_dict:
            error_line = get_error_line(text, index)
            raise ValueError(
                'Missing mandatory parameter "src."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        if "label" not in asy_dict:
            error_line = get_error_line(text, index)
            raise ValueError(
                'Missing mandatory parameter "label."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )

        if asy_dict["label"] in label_list:
            error_line = get_error_line(text, index)
            raise ValueError(
                'Missing mandatory parameter "A diagram with the same filename already exists."'
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )
        # with asy_cache_file.open("r", encoding="utf-8") as f:
        #     asy_cache_content = cast(dict[str, str], json.load(f))
        # if asy_dict["filename"] in asy_cache_content:

    if not (in_dir and out_dir):
        raise TypeError(
            "Input and output directory paths are mandatory arguments."
        )

    build_dir = in_dir / "build/"
    build_dir.mkdir(exist_ok=True)
    asy_cache_file = build_dir / "cache.json"
    if not asy_cache_file.exists():
        asy_cache_file.touch()
        with asy_cache_file.open("w", encoding="utf-8") as f:
            _ = f.write("{}")
