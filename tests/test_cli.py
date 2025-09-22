from pathlib import Path
import tempfile
import shutil
from PIL import Image
from photowatermark.cli import main


def test_cli_dry_run():
    tmp = Path(tempfile.mkdtemp())
    try:
        (tmp / 'a.jpg').write_bytes(b'fake')
        # 不含 EXIF，dry-run 模式只验证扫描
        code = main(['--input', str(tmp), '--dry-run'])
        assert code == 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
