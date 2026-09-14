import re


def get_error_line(text: str, index: int) -> tuple[int, str]:
    line_num = text.count("\n", 0, index)

    return (line_num + 1, text.splitlines()[line_num])


def gobble_inside_delim(
    text: str,
    open_delim_start_index: int,
    open_delim: re.Pattern[str],
    close_delim: re.Pattern[str],
) -> str:
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
            raise RuntimeError("An unexpected error has occured.")

    return index - 1
