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
    tag = tag_and_args[0]
    args = tag_and_args[1]

    content: list[str] = []
    optional_args_list: list[str] = []
    inner_content = gobble_inside_delim(
        text, open_delim_start_index, open_delim, close_delim
    )

    if tag in ["asy", "code", "color", "img", "list", "quote", "url"]:
        if tag == "asy":
            pass

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
            if "hex" not in color_dict:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Missing mandatory parameter "hex."'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )
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
                f'<img src="{inner_content}" {" ".join(optional_args_list)}>'
                if optional_args_list
                else f'<img src="{inner_content}">'
            )
            if "caption" in img_dict:
                content.append(
                    f"<figcaption>{img_dict['caption']}</figcaption>"
                )
            content.append("</figure>")

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
                if "style" not in list_dict:
                    content.append("<ol>")
                else:
                    if list_dict["style"] not in ["1", "A", "a", "I", "i"]:
                        error_line = get_error_line(
                            text, open_delim_start_index
                        )
                        raise ValueError(
                            'Invalid <ol> style provided. Valid ol styles are "1", "A", "a", "I", and "i" only.'
                            + "\n\n"
                            + f"{error_line[0]}: {error_line[1]}"
                        )
                    content.append(f'<ol type="{list_dict["style"]}">')
                content.append(inner_content)
                content.append("</ol>")

            else:
                if "style" not in list_dict:
                    content.append("<ul>")
                else:
                    if list_dict["style"] not in [
                        "disc",
                        "circle",
                        "square",
                        "none",
                    ]:
                        error_line = get_error_line(
                            text, open_delim_start_index
                        )
                        raise ValueError(
                            'Invalid <ul> style provided. Valid ul styles are "disc", "circle", "square", and "none" only.'
                            + "\n\n"
                            + f"{error_line[0]}: {error_line[1]}"
                        )
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
            content.append("<p>" + "\n" + inner_content + "\n" + "</p>")
            content.append("</blockquote>")
            if "author" in quote_dict:
                content.append("<figcaption>")
                content.append("<cite>")
                content.append(quote_dict["author"])
                content.append("</cite>")
                content.append("</figcaption>")
                content.append("</figure>")

        elif tag == "url":
            url_dict = args
            if "link" not in url_dict:
                error_line = get_error_line(text, open_delim_start_index)
                raise ValueError(
                    'Missing mandatory parameter "link."'
                    + "\n\n"
                    + f"{error_line[0]}: {error_line[1]}"
                )
            if "target" in url_dict:
                if url_dict["target"] not in [
                    "self",
                    "blank",
                ]:
                    error_line = get_error_line(text, open_delim_start_index)
                    raise ValueError(
                        'Invalid target value provided. Target can only be "self" or "blank."'
                        + "\n\n"
                        + f"{error_line[0]}: {error_line[1]}"
                    )
                content.append(
                    f'<a href="{url_dict["link"]}" target="_{url_dict["target"]}">'
                )
            content.append(f'<a href="{url_dict["link"]}">')
            content.append(inner_content)
            content.append("</a>")

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
) -> bool:
    tag_and_args = get_tag_and_args(text, open_delim_start_index, open_delim)
    if not tag_and_args[1]:
        return False

    # learning c++ has made me so pedantic that i
    # even wanna optimize this O(mn) search, son ;-;
    for arg in tag_and_args[1]:
        if arg not in valid_args:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                "Invalid argument provided."
                + f"{error_line[0]}: {error_line[1]}"
                + "\n\n"
                + f"{', '.join(valid_args)} are the only valid arguments."
            )

    return True
