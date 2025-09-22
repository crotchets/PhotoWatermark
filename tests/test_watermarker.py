from pathlib import Path
import tempfile
import shutil
from PIL import Image
from photowatermark.watermark_config import WatermarkConfig
from photowatermark.watermarker import apply_watermark


def test_apply_watermark_basic():
    tmp = Path(tempfile.mkdtemp())
    try:
        src = tmp / 'img.jpg'
        Image.new('RGB', (200, 100), color=(128,128,128)).save(src)
        out_dir = tmp / 'out'
        dest = out_dir / 'img.jpg'
        cfg = WatermarkConfig(text='2024-05-06', font_size=24, position='bottom-right')
        apply_watermark(src, dest, cfg)
        assert dest.exists()
        # 简单验证输出尺寸一致
        with Image.open(dest) as im_out, Image.open(src) as im_src:
            assert im_out.size == im_src.size
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
