from pathlib import Path
import sys

# 将 src 目录加入 sys.path，便于直接 import photowatermark
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
