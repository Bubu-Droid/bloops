# API Reference

_Auto-generated from docstrings. Do not edit by hand._

## `bloopser.py`

### `convert_bbcode_to_html` (Function)

Transpile a BBCode string into a complete HTML document.

Iteratively processes configured BBCode tags, converts them into HTML
equivalents, and wraps the result in a boilerplate HTML template
with MathJax and Syntax Highlighting support.

Args:
    text: Raw BBCode text content.
    bbcode_tags: List of tag configurations and rule definitions.

Returns:
    A fully formatted HTML document string.

## `bracer.py`

### `gobble_inside_delim` (Function)

Extract text content located between matching delimiter pairs.

Args:
    text: Input text containing delimited structures.
    open_delim_start_index: Index where the opening tag begins.
    open_delim: Regex pattern matching the opening delimiter.
    close_delim: Regex pattern matching the closing delimiter.

Returns:
    The inner text string enclosed by the matching delimiters.

### `gobble_around_delim` (Function)

Extract text string including the opening and closing delimiters.

Args:
    text: Input text containing delimited structures.
    open_delim_start_index: Index where the opening tag begins.
    open_delim: Regex pattern matching the opening delimiter.
    close_delim: Regex pattern matching the closing delimiter.

Returns:
    Substring spanning from opening tag start to closing tag end.

### `get_close_delim_end_index` (Function)

Find the end index of the matching closing delimiter for a tag.

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

## `validator.py`

### `validate_bbcode` (Function)

Validate BBCode syntax and collect diagram label mappings.

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

### `compile_asy_diagrams` (Function)

Compile Asymptote diagram source blocks into SVG files.

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
