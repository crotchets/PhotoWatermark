from pathlib import Path
import tempfile
import shutil
import pytest
from photowatermark.scanner import scan_directory, SUPPORTED_EXTS


def test_scan_directory_basic():
    tmp = Path(tempfile.mkdtemp())
    try:
        # 创建一些图片和非图片
        (tmp / 'a.jpg').write_bytes(b'fake')
        (tmp / 'b.jpeg').write_bytes(b'fake')
        (tmp / 'c.txt').write_text('not image')
        res = scan_directory(str(tmp))
        names = {p.name for p in res.images}
        assert 'a.jpg' in names and 'b.jpeg' in names and 'c.txt' not in names
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_scan_directory_empty():
    tmp = Path(tempfile.mkdtemp())
    try:
        with pytest.raises(ValueError):
            scan_directory(str(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_scan_directory_not_exist():
    with pytest.raises(FileNotFoundError):
        scan_directory('not_exist_12345')
