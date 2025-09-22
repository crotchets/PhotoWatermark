from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

VALID_POSITIONS = {
    "top-left", "top-center", "top-right",
    "middle-left", "center", "middle-right",
    "bottom-left", "bottom-center", "bottom-right",
}

@dataclass
class WatermarkConfig:
    text: str
    font_size: int = 36
    color: Tuple[int, int, int] = (255, 255, 255)
    opacity: int = 80  # 0-100
    position: str = "bottom-right"
    offset: Tuple[int, int] = (20, 20)  # x, y 像素偏移
    auto_scale: bool = False
    stroke_width: int = 0
    stroke_color: Tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self):
        if self.font_size < 12 or self.font_size > 200:
            raise ValueError("font_size 范围应为 12-200")
        if not (0 <= self.opacity <= 100):
            raise ValueError("opacity 范围应为 0-100")
        if self.position not in VALID_POSITIONS:
            raise ValueError(f"不支持的位置: {self.position}")
        for c in list(self.color) + list(self.stroke_color):
            if not (0 <= c <= 255):
                raise ValueError("颜色通道值应在0-255之间")

__all__ = ["WatermarkConfig", "VALID_POSITIONS"]
