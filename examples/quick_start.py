"""Quick start example for programmatic usage.

Run:
    python examples/quick_start.py -i ./your_photos_dir
"""
from __future__ import annotations
from pathlib import Path
import argparse
from photowatermark.scanner import scan_directory
from photowatermark.exif_reader import extract_date
from photowatermark.watermark_config import WatermarkConfig
from photowatermark.watermarker import apply_watermark


def run(input_dir: str):
    scan_res = scan_directory(input_dir)
    out_dir = scan_res.root / f"{scan_res.root.name}_watermark"
    processed = 0
    for img in scan_res.images:
        date_res = extract_date(img)
        if not date_res.date_text:
            continue
        cfg = WatermarkConfig(text=date_res.date_text, position='bottom-right', font_size=36, opacity=80)
        dest = out_dir / img.relative_to(scan_res.root)
        apply_watermark(img, dest, cfg)
        processed += 1
    print(f"Done. Processed {processed} images. Output: {out_dir}")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input directory of photos')
    args = parser.parse_args(argv)
    run(args.input)


if __name__ == '__main__':
    main()
