# OneNoteExtractor
# Copyright (C) 2023 Volexity, Inc.

"""Example script showing use of OneNoteExtractor."""

import argparse
import logging
import sys
import textwrap
from pathlib import Path

from . import OneNoteExtractor, __version__

logger = logging.getLogger(__name__)


def run() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            f"""
            Volexity OneNote Extractor | Extract metadata and/or files from OneNote files
            Version {__version__}
            https://www.volexity.com
            (C) 2023 Volexity, Inc. All rights reserved"""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("target_file", type=str, help="Input file to parse")
    parser.add_argument("--debug", help="If enabled, sets log level to debug", action="store_true")
    parser.add_argument("--extract-meta", help="If set, extracts metadata from .one file", action="store_true")
    parser.add_argument("--extract-files", help="If set, extracts files from .one file", action="store_true")
    parser.add_argument("--output-directory", help="Where should extracted objects be saved to?", default=Path.cwd())
    parser.add_argument(
        "--password", help="Password to use to extract files from encrypted onenote files", action="store"
    )
    parser.add_argument("--version", action="version", help="print the version of one-extract", version=__version__)
    args = parser.parse_args()

    if not args.extract_meta and not args.extract_files:
        sys.exit("Must either attempt to extract metadata or files.")

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(name)s %(levelname)-8s %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logger.debug("Debug logging enabled.")
    with Path(args.target_file).open("rb") as infile:
        data = infile.read()

    document = OneNoteExtractor(data=data, password=args.password)
    # Extract subfile objects from the document
    if args.extract_files:
        for index, file_data in enumerate(document.extract_files()):
            bn = Path(args.target_file).name
            target_path = Path(args.output_directory) / f"{bn}_{index}.extracted"
            print(f"Writing extracted files to: {target_path}")  # noqa: T201
            with target_path.open("wb") as outf:
                outf.write(file_data)

    # Extract metadata from the document
    if args.extract_meta:
        for on_meta in document.extract_meta():
            print(on_meta)  # noqa: T201
