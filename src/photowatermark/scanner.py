from __future__ import annotations
import os
from pathlib import Path
from typing import List

SUPPORTED_EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".png", ".bmp"}
RAW_EXTS = {".cr2", ".nef", ".arw", ".orf", ".rw2"}  # 基础占位，RAW 格式后续可扩展

class ScanResult:
    def __init__(self, root: Path, images: List[Path]):
        self.root = root
        self.images = images

    def __len__(self):  # 便于直接 len(result)
        return len(self.images)

    def __iter__(self):
        return iter(self.images)


def scan_directory(path_str: str, recursive: bool = True) -> ScanResult:
    """扫描目录并返回图片文件列表。

    :param path_str: 目录路径（可相对可绝对）
    :param recursive: 是否递归扫描子目录
    :raises FileNotFoundError: 路径不存在
    :raises NotADirectoryError: 不是目录
    :raises PermissionError: 访问权限不足
    :raises ValueError: 没有找到任何图片文件
    """
    p = Path(path_str).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"路径不存在: {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"不是有效的目录: {p}")

    # 访问测试
    if not os.access(p, os.R_OK):
        raise PermissionError(f"没有读取权限: {p}")

    patterns = ["*"] if recursive else ["*"]  # 可按需扩展
    images: List[Path] = []
    for dirpath, _dirnames, filenames in os.walk(p):
        for name in filenames:
            ext = name.lower().rsplit('.', 1)[-1] if '.' in name else ''
            dot_ext = f".{ext}"
            if dot_ext in SUPPORTED_EXTS or dot_ext in RAW_EXTS:
                images.append(Path(dirpath) / name)
        if not recursive:
            break

    if not images:
        raise ValueError(f"目录内未找到可处理的图片文件: {p}")

    # 排序保证稳定性
    images.sort()
    return ScanResult(root=p, images=images)

__all__ = ["scan_directory", "ScanResult", "SUPPORTED_EXTS", "RAW_EXTS"]
