# Throwaway script by Claude.

import ast
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent.parent
SRC_DIR: Path = REPO_ROOT / "src" / "bloops"
OUTPUT_FILE: Path = REPO_ROOT / "docs" / "API.md"

MISSING_DOCSTRING_NOTICE: str = "⚠️ **No docstring — needs manual review.**"


def extract_docs(file_path: Path) -> list[str]:
    tree: ast.Module = ast.parse(file_path.read_text(encoding="utf-8"))
    lines: list[str] = []
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            if node.name.startswith("_"):
                continue
            docstring: str | None = ast.get_docstring(node)
            kind: str = (
                "Class" if isinstance(node, ast.ClassDef) else "Function"
            )
            lines.append(f"### `{node.name}` ({kind})\n")
            lines.append(
                f"{docstring if docstring else MISSING_DOCSTRING_NOTICE}\n"
            )
    return lines


def is_private_path(path: Path, root: Path) -> bool:
    for part in path.relative_to(root).parts:
        name: str = part.removesuffix(".py")
        if name.startswith("_"):
            return True
    return False


def main() -> None:
    all_lines: list[str] = [
        "# API Reference\n",
        "_Auto-generated from docstrings. Do not edit by hand._\n",
    ]
    for py_file in sorted(SRC_DIR.rglob("*.py")):
        if is_private_path(py_file, SRC_DIR):
            continue

        docs: list[str] = extract_docs(py_file)
        if docs:
            all_lines.append(f"## `{py_file.relative_to(SRC_DIR)}`\n")
            all_lines.extend(docs)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    _ = OUTPUT_FILE.write_text("\n".join(all_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
