import argparse
import pathlib
from typing import cast

from . import builder

# TODO: ensure that the description here matches with that in the github repo desc
parser = argparse.ArgumentParser(
    prog="bloops",
    description="A BBCode to HTML transpiler written in Python with support for Asymptote geometry diagrams.",
    allow_abbrev=False,
)

# TODO: maybe add a version argument if i make this a package later on

build_group = parser.add_mutually_exclusive_group()

_ = build_group.add_argument(
    "-b",
    "--build",
    action="store_true",
    help="convert BBCode to HTML and write to index.html",
)
_ = build_group.add_argument(
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
    nargs=1,
    type=pathlib.Path,
    required=True,
    metavar="OUTDIR",
    help="directory path where generated Asymptote diagrams are to be saved",
)

args = parser.parse_args()

in_dir = cast(pathlib.Path, args.input[0])
out_dir = cast(pathlib.Path, args.output[0])
build_flag = cast(bool, args.build)
cont_build_flag = cast(bool, args.build_cont)

if build_flag:
    builder.main(in_dir, out_dir)
if cont_build_flag:
    builder.main(in_dir, out_dir, build_cont=True)
