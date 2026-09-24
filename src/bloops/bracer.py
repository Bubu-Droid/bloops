"""Utility functions for parsing nested delimiter pairs and tags."""

import re

from bloops._helper import get_error_line


def gobble_inside_delim(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
) -> str:
    """Extract text content located between matching delimiter pairs.

    Args:
        text: Input text containing delimited structures.
        open_delim_start_index: Index where the opening tag begins.
        open_delim: Regex pattern matching the opening delimiter.
        close_delim: Regex pattern matching the closing delimiter.

    Returns:
        The inner text string enclosed by the matching delimiters.
    """

    close_delim_end_index = get_close_delim_end_index(
        text, open_delim_start_index, open_delim, close_delim
    )
    close_delim_start_index = text.rindex(
        "[/", open_delim_start_index, close_delim_end_index
    )
    open_pair_end_index = get_close_delim_end_index(
        text, open_delim_start_index, re.compile(r"\["), re.compile(r"\]")
    )

    return text[open_pair_end_index + 1 : close_delim_start_index]


def gobble_around_delim(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
) -> str:
    """Extract text string including the opening and closing delimiters.

    Args:
        text: Input text containing delimited structures.
        open_delim_start_index: Index where the opening tag begins.
        open_delim: Regex pattern matching the opening delimiter.
        close_delim: Regex pattern matching the closing delimiter.

    Returns:
        Substring spanning from opening tag start to closing tag end.
    """

    close_delim_end_index = get_close_delim_end_index(
        text, open_delim_start_index, open_delim, close_delim
    )

    return text[open_delim_start_index : close_delim_end_index + 1]


def get_close_delim_end_index(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
) -> int:
    """Find the end index of the matching closing delimiter for a tag.

    Supports nested tag pairs by maintaining a count of open and close
    delimiters.

    Args:
        text: Full input text being parsed.
        open_delim_start_index: Index where opening delimiter begins.
        open_delim: Regex pattern matching opening delimiters.
        close_delim: Regex pattern matching closing delimiters.

    Returns:
        The index of the final character of the matching closing tag.

    Raises:
        SyntaxError: If no opening tag exists at the index or if a
            matching closing tag cannot be found.
        RuntimeError: If parser enters an unexpected state.
    """

    open_delim_counter = 1
    close_delim_counter = 0

    match = open_delim.match(text, open_delim_start_index)

    if not match:
        error_line = get_error_line(text, open_delim_start_index)
        raise SyntaxError(
            "No opening delimiter at the current position."
            + "\n\n"
            + f"{error_line[0]}: {error_line[1]}"
        )

    index = match.end()

    while open_delim_counter > close_delim_counter:
        open_delim_match = open_delim.search(text, index)
        close_delim_match = close_delim.search(text, index)

        if not close_delim_match:
            error_line = get_error_line(text, index - 1)
            raise SyntaxError(
                "Failed to find an opening pair for delimiter."
                + "\n\n"
                + f"{error_line[0]}: {error_line[1]}"
            )

        elif not open_delim_match:
            index = close_delim_match.end()
            close_delim_counter += 1
        elif open_delim_match.start() < close_delim_match.start():
            index = open_delim_match.end()
            open_delim_counter += 1
        elif close_delim_match.start() < open_delim_match.start():
            index = close_delim_match.end()
            close_delim_counter += 1
        else:
            raise RuntimeError("An unexpected error has occurred.")

    return index - 1
