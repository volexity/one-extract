from pathlib import Path

import pytest

from one_extract import OneNoteExtractor


def test_extract_example() -> None:
    path = Path(__file__).parent / "files" / "example.one"
    with path.open("rb") as f:
        data = f.read()

    document = OneNoteExtractor(data=data)
    if document._is_password_protected():  # noqa: SLF001
        pytest.fail("example.one should not be password protected")

    files = list(document.extract_files())
    assert len(files) == 1
