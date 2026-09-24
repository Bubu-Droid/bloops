"""Helper routines for text parsing and line error retrieval."""

import re


def get_error_line(text: str, index: int) -> tuple[int, str]:
    """Locate the line number and text line corresponding to an index.

    Args:
        text: Entire string content.
        index: Character index within the text.

    Returns:
        A tuple containing the 1-based line number and line text string.
    """

    line_num = text.count("\n", 0, index)

    return (line_num + 1, text.splitlines()[line_num])


def get_tag_and_args(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
) -> tuple[str, dict[str, str]]:
    """Extract the tag name and attribute dictionary from an open tag.

    Args:
        text: Input text containing the tag.
        open_delim_start_index: Character index where tag begins.
        open_delim: Pattern matching the opening tag structure.

    Returns:
        A tuple containing the tag name and a dictionary of argument
        key-value pairs.

    Raises:
        SyntaxError: If no valid match is found at the given index.
    """

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
