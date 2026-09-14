import argparse
import pathlib
from typing import cast

from . import build_and_preview

# TODO: ensure that the description here matches with that in the github repo desc
parser = argparse.ArgumentParser(
    prog="bloops",
    description="A BBCode to HTML transpiler written in Python with support for Asymptote geometry diagrams.",
    allow_abbrev=False,
)

# TODO: maybe add a version argument if i make this a package later on

_ = parser.add_argument(
    "-c",
    "--build-cont",
    action="store_true",
    help="convert BBCode to HTML and continuously write to index.html on change",
)
_ = parser.add_argument(
    "-p",
    "--preview",
    action="store_true",
    help="run a preview of index.html on the web-browser",
)
_ = parser.add_argument(
    "-i",
    "--input",
    action="store",
    nargs=1,
    type=pathlib.Path,
    required=True,
    metavar="INDIR",
    help="directory path which contains the BBCode file",
)
_ = parser.add_argument(
    "-o",
    "--output",
    action="store",
    nargs="?",
    type=pathlib.Path,
    metavar="OUTDIR",
    help="optional directory path where generated Asymptote diagrams are to be saved",
)

args = parser.parse_args()

# I LOVE TYPE HINTING!!!!
in_dir = cast(pathlib.Path, args.input[0])
out_arg = cast(pathlib.Path | None, args.output)
out_dir = out_arg if out_arg and out_arg else in_dir / "static/"

build_cont_flag = cast(bool, args.build_cont)
preview_flag = cast(bool, args.preview)

build_and_preview.main(
    in_dir, out_dir, build_cont=build_cont_flag, preview=preview_flag
)
