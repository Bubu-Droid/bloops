from pathlib import Path

from bloops.bloopser import convert_bbcode_to_html
from bloops.validator import validate_bbcode

REPO_ROOT: Path = Path(__file__).resolve().parent.parent.parent
INPUT_FILE: Path = REPO_ROOT / "examples" / "content.bbcode"
OUTPUT_FILE: Path = REPO_ROOT / "index.html"


def main() -> None:
    bbcode_source: str = INPUT_FILE.read_text(encoding="utf-8")
    _ = validate_bbcode(bbcode_source)
    html_output: str = convert_bbcode_to_html(bbcode_source)
    _ = OUTPUT_FILE.write_text(html_output, encoding="utf-8")


if __name__ == "__main__":
    main()
