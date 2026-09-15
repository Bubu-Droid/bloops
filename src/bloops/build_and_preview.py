import pathlib
import threading
import time
from typing import override

from livereload import Server  # pyright: ignore[reportMissingTypeStubs]
from watchdog.events import (
    DirModifiedEvent,
    FileModifiedEvent,
    PatternMatchingEventHandler,
)
from watchdog.observers import Observer

from bloops.bloopser import transpile_all_tags
from bloops.validator import validate_tags_and_setup_asy
from bloops.vars import ERROR_CODE, STYLESHEET


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
        self.input_file: pathlib.Path = in_dir / "content.bbcode"
        self.file_content: str = file_content
        self.output_file: pathlib.Path = in_dir / "index.html"
        self._build()
        print("Build successful. Output written to index.html.\n")

    @override
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        with self.input_file.open(mode="r", encoding="utf-8") as f:
            new_content = f.read().strip()
        if self.file_content == new_content:
            return
        print("---------- File change detected ----------")
        self.file_content = new_content
        self._build()
        print("Build successful. Output written to index.html.")
        print("Watching for file update. Use ctrl/C to stop...\n")

    def _build(self) -> None:
        try:
            print(
                "Verifying syntax and generating newly added / changed asymptote diagrams (if any)..."
            )
            validate_tags_and_setup_asy(
                self.file_content, self.in_dir, self.out_dir
            )

            print("Converting BBCODE into HTML...")
            with self.output_file.open("w", encoding="utf-8") as f:
                _ = f.write(transpile_all_tags(self.file_content))
        except Exception as e:
            with self.output_file.open("w", encoding="utf-8") as f:
                _ = f.write(ERROR_CODE)
            # HACK: the liveserver plugin takes short time span before
            # it can reflect the updates.
            # if we raise the exception immediately, then the program
            # terminates before even we are able to reflect the error
            # message
            # a fix would really be appreciated. help me fix this, anon.
            time.sleep(1)
            raise e


def main(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    build_cont: bool = False,
    preview: bool = False,
) -> None:
    input_file = in_dir / "content.bbcode"
    output_file = in_dir / "index.html"
    style_file = out_dir / "style.css"

    if not in_dir.exists():
        raise FileNotFoundError("Input directory not found.")
    if not in_dir.is_dir():
        raise NotADirectoryError("Input directory is not a directory.")
    if not input_file.exists():
        raise FileNotFoundError("BBCode file (content.bbcode) not found.")
    if not out_dir.exists():
        # raise FileNotFoundError("Output directory not found.")
        out_dir.mkdir()
    if not out_dir.is_dir():
        raise NotADirectoryError("Output directory is not a directory.")
    with input_file.open(mode="r", encoding="utf-8") as f:
        file_content = f.read().strip()
    if not style_file.exists():
        with style_file.open("w", encoding="utf-8") as f:
            _ = f.write(STYLESHEET)

    handler = Handler(in_dir, out_dir, file_content)

    if preview:
        server_thread = threading.Thread(
            target=run_server, daemon=True, args=(output_file,)
        )
        server_thread.start()

    if build_cont:
        observer = Observer()
        src_path = str(in_dir)
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


# why the fuck does livereload not use type-hinting?
# alright, i've opened an issue and i'll try adding type-hint support
# if no one else does
def run_server(output_file: pathlib.Path) -> None:
    server = Server()
    server.watch(str(output_file.absolute()))  # pyright: ignore[reportUnknownMemberType]
    server.serve(root=str(output_file.parent.resolve()))  # pyright: ignore[reportUnknownMemberType]
