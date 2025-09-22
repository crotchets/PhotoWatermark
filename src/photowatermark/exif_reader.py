from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional
from PIL import Image, ExifTags

# 反向映射 EXIF 标签
EXIF_TAGS = {v: k for k, v in ExifTags.TAGS.items()}
_DATE_KEYS = [
    EXIF_TAGS.get("DateTimeOriginal"),
    EXIF_TAGS.get("DateTimeDigitized"),
    EXIF_TAGS.get("DateTime"),
]

class ExifDateResult:
    def __init__(self, path: Path, date_text: Optional[str]):
        self.path = path
        self.date_text = date_text  # YYYY-MM-DD 或 None

    def __repr__(self):
        return f"ExifDateResult(path={self.path.name}, date_text={self.date_text})"


def extract_date(path: Path) -> ExifDateResult:
    """提取图片拍摄日期，格式 YYYY-MM-DD。若无可用日期返回 None。"""
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            if not exif:
                return ExifDateResult(path, None)
            for key in filter(None, _DATE_KEYS):
                raw = exif.get(key)
                if raw:
                    # EXIF 时间格式通常为 'YYYY:MM:DD HH:MM:SS'
                    try:
                        dt = datetime.strptime(str(raw), "%Y:%m:%d %H:%M:%S")
                        return ExifDateResult(path, dt.strftime("%Y-%m-%d"))
                    except Exception:
                        continue
    except Exception:
        return ExifDateResult(path, None)
    return ExifDateResult(path, None)

__all__ = ["extract_date", "ExifDateResult"]
