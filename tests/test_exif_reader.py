from pathlib import Path
import tempfile
import shutil
from PIL import Image
import pytest
from photowatermark.exif_reader import extract_date


def _create_jpeg_with_exif(path: Path, dt: str):
    # 创建一个简单的带 EXIF 的 JPEG
    img = Image.new('RGB', (10, 10), color=(255, 0, 0))
    exif_dict = img.getexif()
    # EXIF 36867: DateTimeOriginal
    exif_dict[36867] = dt  # 'YYYY:MM:DD HH:MM:SS'
    img.save(path, exif=exif_dict)


def test_extract_date_ok():
    tmp = Path(tempfile.mkdtemp())
    try:
        target = tmp / 't.jpg'
        _create_jpeg_with_exif(target, '2023:07:05 10:11:12')
        res = extract_date(target)
        assert res.date_text == '2023-07-05'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_extract_date_missing():
    tmp = Path(tempfile.mkdtemp())
    try:
        target = tmp / 't2.jpg'
        Image.new('RGB', (5,5), color=(0,0,0)).save(target)
        res = extract_date(target)
        assert res.date_text is None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
