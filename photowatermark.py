"""便捷运行入口。

等价执行:  python -m src.photowatermark.cli  或  python photowatermark.py --input <dir>

示例:
	python photowatermark.py --input examples/images --font-size 42 --position bottom-right --opacity 80
"""
from __future__ import annotations
import sys
from pathlib import Path

# 将 src 目录加入 sys.path 以便直接 import
ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
	sys.path.insert(0, str(SRC))

from photowatermark.cli import main  # type: ignore  # noqa: E402

if __name__ == '__main__':
	raise SystemExit(main())

