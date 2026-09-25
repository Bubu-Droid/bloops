"""Validation and diagram compilation utilities for BBCode tags.

Verifies element parameters, enforces structural constraints, and
compiles Asymptote diagrams to SVG format.
"""

import json
import pathlib
import re
import subprocess
from typing import cast

from bloops._helper import get_error_line, get_tag_and_args
from bloops.bracer import (
    get_close_delim_end_index,
    gobble_inside_delim,
)
from bloops.vars import BBCODE_TAGS


def validate_bbcode(
    text: str,
    bbcode_tags: list[
        tuple[re.Pattern[str], re.Pattern[str], list[str]]
    ] = BBCODE_TAGS,
) -> dict[str, int]:
    """Validate BBCode syntax and collect diagram label mappings.

    Scans the input string for supported BBCode tags, validates their
    attributes, checks for duplicate Asymptote labels, and returns a
    dictionary mapping each diagram label to its character index.

    Args:
        text: Raw BBCode input string.
        bbcode_tags: List of tag configurations, matching patterns,
            and permitted argument lists.

    Returns:
        A dictionary mapping diagram labels to their starting index.

    Raises:
        ValueError: If an invalid argument is supplied or duplicate
            diagram labels are encountered.
    """

    label_dict: dict[str, int] = {}
    for tag_tuple in bbcode_tags:
        open_delim = tag_tuple[0]
        valid_args = tag_tuple[2]
        index = 0
        match = open_delim.search(text, index)
        # TODO: fix this hack after changing BBCODE_TAGS to dict
        is_asy = bool("label" in valid_args)
        while match:
            index = match.start()
            _ = get_close_delim_end_index(
                text, index, tag_tuple[0], tag_tuple[1]
            )
            _validate_args(text, index, open_delim, valid_args)
            if is_asy:
                args = get_tag_and_args(text, index, open_delim)[1]
                if args["label"] in label_dict:
                    error_line = get_error_line(text, index)
                    raise ValueError(
                        "A diagram with the same label already exists."
                        + "\n\n"
                        + f"{error_line[0]}: {error_line[1]}"
                    )
                label_dict[args["label"]] = index
            match = open_delim.search(text, match.end())

    return label_dict


def compile_asy_diagrams(
    label_dict: dict[str, int],
    text: str,
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
) -> None:
    """Compile Asymptote diagram source blocks into SVG files.

    Checks diagram source strings against a local JSON cache, writing
    and rendering updated or new `.asy` files via the external Asymptote
    CLI.

    Args:
        label_dict: Dictionary mapping diagram labels to character
            indices in the source text.
        text: Entire input text containing BBCode and Asymptote code.
        in_dir: Source directory containing the build cache folder.
        out_dir: Target directory where compiled SVG images are stored.

    Raises:
        ValueError: If Asymptote compilation fails.
    """

    build_dir = in_dir / "build/"
    asy_cache_file = build_dir / "cache.json"
    with asy_cache_file.open("r", encoding="utf-8") as f:
        asy_cache_content = cast(dict[str, str], json.load(f))

    for label, index in label_dict.items():
        changed = False
        # TODO: ensure that we remove this hardcoded patterns after changing
        # BBCODE_TAGS to a dict
        inner_content = gobble_inside_delim(
            text,
            index,
            re.compile(r"\[(asy)(.*?)\]"),
            re.compile(r"\[/asy\]"),
        ).strip()
        if label not in asy_cache_content:
            asy_cache_content[label] = inner_content
            changed = True
        else:
            if asy_cache_content[label] != inner_content:
                asy_cache_content[label] = inner_content
                changed = True
        if changed:
            asy_code_file = build_dir / f"{label}.asy"
            with asy_code_file.open("w", encoding="utf-8") as f:
                _ = f.write(inner_content)

            res = subprocess.run(
                [
                    "asy",
                    asy_code_file.absolute(),
                    "-f",
                    "svg",
                    "-o",
                    (out_dir / label).absolute(),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if res.returncode == 0:
                with asy_cache_file.open("w", encoding="utf-8") as f:
                    json.dump(asy_cache_content, f)
            else:
                error_line = get_error_line(text, index)
                error_message = res.stderr
                raise ValueError(
                    f"{error_line[0]}: {error_line[1]}" + "\n\n" + error_message
                )


def _validate_args(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    valid_args: list[str],
) -> None:
    """Validate arguments and mandatory attributes for a BBCode tag.

    Args:
        text: Entire input text containing the BBCode.
        open_delim_start_index: Starting character index of opening tag.
        open_delim: Compiled regex pattern for the opening tag.
        valid_args: List of valid attribute names for the tag.

    Raises:
        ValueError: If unknown attributes or missing required parameters
            are encountered, or if attribute values are invalid.
    """

    tag_and_args = get_tag_and_args(text, open_delim_start_index, open_delim)
    tag, args = tag_and_args

    for arg in args:
        if arg not in valid_args:
            error_line = get_error_line(text, open_delim_start_index)
            raise ValueError(
                f"Invalid argument provided. {', '.join(valid_args)} are the only valid arguments."
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
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
