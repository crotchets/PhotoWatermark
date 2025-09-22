from __future__ import annotations
import sys
from pathlib import Path
import argparse
from typing import Optional
from .scanner import scan_directory
from .exif_reader import extract_date
from .watermark_config import WatermarkConfig
from .watermarker import apply_watermark

try:
    from tqdm import tqdm  # 可选进度条
except Exception:  # 若未安装则定义占位
    def tqdm(iterable, **_):
        return iterable


def parse_color(color_str: str):
    parts = [p.strip() for p in color_str.split(',')]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("颜色需要3个逗号分隔整数，如 255,255,255")
    try:
        r, g, b = map(int, parts)
    except ValueError:
        raise argparse.ArgumentTypeError("颜色值必须为整数")
    for v in (r, g, b):
        if not (0 <= v <= 255):
            raise argparse.ArgumentTypeError("颜色通道值应在0-255之间")
    return (r, g, b)


def build_parser():
    parser = argparse.ArgumentParser(description="为图片批量添加EXIF日期水印")
    parser.add_argument('--input', '-i', required=True, help='图片目录路径')
    parser.add_argument('--font-size', type=int, default=36, help='字体大小 (12-200)')
    parser.add_argument('--color', type=parse_color, default=(255, 255, 255), help='RGB颜色, 例: 255,255,255')
    parser.add_argument('--position', default='bottom-right', help='水印位置, 例如 bottom-right')
    parser.add_argument('--opacity', type=int, default=80, help='透明度 0-100')
    parser.add_argument('--offset', default='20,20', help='偏移量 x,y 例: 20,20')
    parser.add_argument('--auto-scale', action='store_true', help='根据图片尺寸自动缩放字体')
    parser.add_argument('--stroke-width', type=int, default=0, help='文字描边宽度')
    parser.add_argument('--stroke-color', type=parse_color, default=(0,0,0), help='文字描边颜色')
    parser.add_argument('--font-path', help='自定义字体文件路径 TTF/OTF')
    parser.add_argument('--recursive', action='store_true', help='递归扫描子目录')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要处理的文件，不输出')
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        offset_parts = [int(x) for x in args.offset.split(',')]
        if len(offset_parts) != 2:
            raise ValueError
        offset = (offset_parts[0], offset_parts[1])
    except Exception:
        parser.error('offset 参数格式错误，应为 x,y')
        return 1

    try:
        scan_res = scan_directory(args.input, recursive=args.recursive)
    except Exception as e:
        parser.error(str(e))
        return 2

    output_dir = scan_res.root / f"{scan_res.root.name}_watermark"

    if args.dry_run:
        print(f"即将处理 {len(scan_res)} 张图片，输出目录: {output_dir}")
        for p in scan_res.images[:10]:
            print("示例:", p.name)
        return 0

    for img_path in tqdm(scan_res.images, desc="处理", unit="张"):
        exif_res = extract_date(img_path)
        if not exif_res.date_text:
            # 跳过无日期图片：可以扩展为使用文件修改时间
            continue
        cfg = WatermarkConfig(
            text=exif_res.date_text,
            font_size=args.font_size,
            color=args.color,
            opacity=args.opacity,
            position=args.position,
            offset=offset,
            auto_scale=args.auto_scale,
            stroke_width=args.stroke_width,
            stroke_color=args.stroke_color,
        )
        rel = img_path.relative_to(scan_res.root)
        dest = output_dir / rel
        try:
            apply_watermark(img_path, dest, cfg, font_path=args.font_path)
        except Exception as e:
            print(f"[警告] 处理失败 {img_path.name}: {e}")

    print(f"完成，输出目录: {output_dir}")
    return 0


if __name__ == '__main__':  # 允许直接运行
    raise SystemExit(main())
