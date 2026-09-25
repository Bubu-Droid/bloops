"""Provides live-reloading and continuous building capabilities.

Monitors file system modifications in input directories and updates
rendered HTML documents or serves them over a local development
server.
"""

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

from bloops.bloopser import convert_bbcode_to_html
from bloops.validator import compile_asy_diagrams, validate_bbcode
from bloops.vars import ERROR_TEMPLATE, STYLESHEET


class _Handler(PatternMatchingEventHandler):
    """Custom event handler for file system modification events.

    Listens for changes in the BBCode source file and triggers a rebuild
    of the rendered HTML and dependent diagram assets.

    Attributes:
        in_dir: Directory path containing the source BBCode file.
        out_dir: Output directory path for static assets.
        input_file: Path to the BBCode source file.
        output_file: Path to the destination HTML file.
        file_content: Cached string content of the source file.
    """

    def __init__(
        self, in_dir: pathlib.Path, out_dir: pathlib.Path, file_content: str
    ) -> None:
        """Initialize the file watcher event handler and perform an initial build.

        Args:
            in_dir: Path to the directory containing input files.
            out_dir: Path to the directory for compiled static output.
            file_content: Initial text content of the BBCode file.
        """

        super().__init__(
            patterns=["content.bbcode"],
            ignore_directories=True,
            case_sensitive=True,
        )
        self.in_dir: pathlib.Path = in_dir
        self.out_dir: pathlib.Path = out_dir
        self.input_file: pathlib.Path = in_dir / "content.bbcode"
        self.output_file: pathlib.Path = in_dir / "index.html"
        self.file_content: str = file_content
        self._build()
        print("Build successful. Output written to index.html.\n")

    @override
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        """Handle file or directory modification events.

        Reads the updated source file, compares it against cached content,
        and re-runs the build process if changes are detected.

        Args:
            event: File system event describing the modification.
        """

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
        """Validate BBCode syntax, compile diagrams, and output HTML.

        Catches rendering errors and writes a predefined error template to
        the output file if compilation fails.

        Raises:
            Exception: Re-raises any syntax or compilation exception encountered
                during execution.
        """

        try:
            print(
                "Verifying syntax and generating newly added / changed asymptote diagrams (if any)..."
            )
            compile_asy_diagrams(
                validate_bbcode(self.file_content),
                self.file_content,
                self.in_dir,
                self.out_dir,
            )

            print("Converting BBCode into HTML...")
            with self.output_file.open("w", encoding="utf-8") as f:
                _ = f.write(convert_bbcode_to_html(self.file_content))
        except Exception:
            with self.output_file.open("w", encoding="utf-8") as f:
                _ = f.write(ERROR_TEMPLATE)
            # HACK: the liveserver plugin takes short time span before
            # it can reflect the updates.
            # if we raise the exception immediately, then the program
            # terminates before even we are able to reflect the error
            # message
            # a fix would really be appreciated. help me fix this, anon.
            time.sleep(1)
            raise


def main(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    build_cont: bool = False,
    preview: bool = False,
) -> None:
    """Coordinate continuous build tasks and local server preview.

    Ensures required directories and default files exist, sets up
    file watchers, and optionally serves content using a live-reload
    server.

    Args:
        in_dir: Directory path containing source files.
        out_dir: Directory path for generated output assets.
        build_cont: If True, continuously watch for source changes.
        preview: If True, launch a local web server for live preview.

    Raises:
        FileNotFoundError: If the input directory or source file is missing.
        NotADirectoryError: If specified paths are not valid directories.
    """

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
        out_dir.mkdir()
    if not out_dir.is_dir():
        raise NotADirectoryError("Output directory is not a directory.")
    with input_file.open(mode="r", encoding="utf-8") as f:
        file_content = f.read().strip()
    if not style_file.exists():
        with style_file.open("w", encoding="utf-8") as f:
            _ = f.write(STYLESHEET)

    handler = _Handler(in_dir, out_dir, file_content)

    if preview:
        if build_cont:
            server_thread = threading.Thread(
                target=_run_server, daemon=False, args=(output_file,)
            )
            server_thread.start()
        else:
            print("Press ctrl/C to stop preview.\n")
            _run_server(output_file)

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
def _run_server(output_file: pathlib.Path) -> None:
    """Start a local web server with automatic browser live-reload.

    Args:
        output_file: Path to the HTML file to watch and serve.
    """
    server = Server()
    server.watch(str(output_file.absolute()))  # pyright: ignore[reportUnknownMemberType]
    server.serve(root=str(output_file.parent.resolve()))  # pyright: ignore[reportUnknownMemberType]
