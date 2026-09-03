import pathlib
from typing import override

from watchdog.events import (
    DirModifiedEvent,
    FileModifiedEvent,
    PatternMatchingEventHandler,
)
from watchdog.observers import Observer

from bloops.bloopser import transpile_all_tags
from bloops.validator import validate_tags_and_setup_asy


class Handler(PatternMatchingEventHandler):
    def __init__(
        self, in_dir: pathlib.Path, out_dir: pathlib.Path, file_content: str
    ) -> None:
        super().__init__(
            patterns=["content.bbcode"],
            ignore_directories=True,
            case_sensitive=True,
        )
        self.in_dir: pathlib.Path = in_dir
        self.out_dir: pathlib.Path = out_dir
        self.file_path: pathlib.Path = in_dir / "content.bbcode"
        self.file_content: str = file_content
        self.output_file: pathlib.Path = in_dir / "index.html"
        self._build()
        print("Build successful. Output written to index.html.\n")

    @override
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        with self.file_path.open(mode="r", encoding="utf-8") as f:
            new_content = f.read().strip()
        if self.file_content == new_content:
            return
        print("---------- File change detected ----------")
        self.file_content = new_content
        self._build()
        print("Build successful. Output written to index.html.")
        print("Watching for file update. Use ctrl/C to stop...\n")

    def _build(self) -> None:
        print(
            "Verifying syntax and generating newly added / changed asymptote diagrams (if any)..."
        )
        validate_tags_and_setup_asy(
            self.file_content, self.in_dir, self.out_dir
        )

        print("Converting BBCODE into HTML...")
        with self.output_file.open("w", encoding="utf-8") as f:
            _ = f.write(transpile_all_tags(self.file_content))


def main(
    in_dir: pathlib.Path, out_dir: pathlib.Path, build_cont: bool = False
) -> None:
    in_dir_abs = in_dir.absolute()
    out_dir_abs = out_dir.absolute()

    if not in_dir_abs.exists():
        raise FileNotFoundError("Input directory not found.")
    if not in_dir_abs.is_dir():
        raise NotADirectoryError("Input directory is not a directory.")
    file_path = in_dir_abs / "content.bbcode"
    if not file_path.exists():
        raise FileNotFoundError("BBCode file (content.bbcode) not found.")
    if not out_dir_abs.exists():
        raise FileNotFoundError("Output directory not found.")
    if not out_dir_abs.is_dir():
        raise NotADirectoryError("Output directory is not a directory.")
    with file_path.open(mode="r", encoding="utf-8") as f:
        file_content = f.read().strip()

    handler = Handler(in_dir_abs, out_dir_abs, file_content)

    if build_cont:
        observer = Observer()
        src_path = str(in_dir_abs)
        _ = observer.schedule(handler, path=src_path, recursive=False)
        observer.start()
        print("Watching for file update. Use ctrl/C to stop...\n")
        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            print("User typed ctrl/C or ctrl/break.  I'll finish.")
        finally:
            observer.stop()
            observer.join()
