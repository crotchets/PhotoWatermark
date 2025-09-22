from __future__ import annotations
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from .watermark_config import WatermarkConfig

try:
    DEFAULT_FONT = ImageFont.load_default()
except Exception:  # fallback
    DEFAULT_FONT = None


def _calc_position(base_w: int, base_h: int, text_w: int, text_h: int, position: str, offset: Tuple[int, int]):
    ox, oy = offset
    if position == "top-left":
        return ox, oy
    if position == "top-center":
        return (base_w - text_w) // 2, oy
    if position == "top-right":
        return base_w - text_w - ox, oy
    if position == "middle-left":
        return ox, (base_h - text_h) // 2
    if position == "center":
        return (base_w - text_w) // 2, (base_h - text_h) // 2
    if position == "middle-right":
        return base_w - text_w - ox, (base_h - text_h) // 2
    if position == "bottom-left":
        return ox, base_h - text_h - oy
    if position == "bottom-center":
        return (base_w - text_w) // 2, base_h - text_h - oy
    if position == "bottom-right":
        return base_w - text_w - ox, base_h - text_h - oy
    return ox, oy


def apply_watermark(src: Path, dest: Path, cfg: WatermarkConfig, font_path: str | None = None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src).convert("RGBA") as im:
        base_w, base_h = im.size

        # 自动缩放字体
        font_size = cfg.font_size
        if cfg.auto_scale:
            font_size = max(12, int(min(base_w, base_h) * 0.04))

        font = DEFAULT_FONT
        if font_path and Path(font_path).exists():
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                font = DEFAULT_FONT
        elif hasattr(ImageFont, 'truetype'):
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except Exception:
                font = DEFAULT_FONT

        txt_layer = Image.new("RGBA", im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        text = cfg.text
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=cfg.stroke_width)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        x, y = _calc_position(base_w, base_h, text_w, text_h, cfg.position, cfg.offset)

        fill_rgba = (*cfg.color, int(255 * (cfg.opacity / 100.0)))
        stroke_fill = (*cfg.stroke_color, int(255 * (cfg.opacity / 100.0))) if cfg.stroke_width > 0 else None
        draw.text((x, y), text, font=font, fill=fill_rgba, stroke_width=cfg.stroke_width, stroke_fill=stroke_fill)

        combined = Image.alpha_composite(im, txt_layer)
        # 输出使用原格式（若支持）
        out_format = im.format or 'PNG'
        if out_format.upper() == 'JPEG':  # 去除 alpha
            combined = combined.convert('RGB')
        combined.save(dest, quality=95)

__all__ = ["apply_watermark"]
