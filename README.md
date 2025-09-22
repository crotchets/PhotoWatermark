# PhotoWatermark

基于 EXIF 拍摄日期的批量图片文字水印工具。

## 功能特性
- 批量扫描目录图片（支持 JPG/JPEG/PNG/TIFF 等）
- 提取 EXIF DateTimeOriginal 并格式化为 `YYYY-MM-DD`
- 可配置：字体大小、颜色、透明度、九宫格位置、偏移、自动缩放、描边
- 输出到 `<原目录名>_watermark` 子目录，保持原文件名
- CLI 或 Python 代码方式调用

## 安装
```bash
pip install -r requirements.txt
```

## 命令行使用
```bash
python -m photowatermark.cli \
	--input ./photos \
	--font-size 48 \
	--color 255,255,255 \
	--position bottom-right \
	--opacity 80 \
	--stroke-width 2 \
	--stroke-color 0,0,0
```

Dry-run 查看扫描结果：
```bash
python -m photowatermark.cli -i ./photos --dry-run
```

递归处理子目录：
```bash
python -m photowatermark.cli -i ./photos --recursive
```

## Python 编程方式示例
见 `examples/quick_start.py`，或直接：
```python
from photowatermark.scanner import scan_directory
from photowatermark.exif_reader import extract_date
from photowatermark.watermark_config import WatermarkConfig
from photowatermark.watermarker import apply_watermark

scan_res = scan_directory('./photos')
out_dir = scan_res.root / f"{scan_res.root.name}_watermark"
for img in scan_res.images:
		exif_res = extract_date(img)
		if not exif_res.date_text:
				continue
		cfg = WatermarkConfig(text=exif_res.date_text, position='bottom-right')
		dest = out_dir / img.relative_to(scan_res.root)
		apply_watermark(img, dest, cfg)
print('done')
```

## 位置参数说明
`top-left | top-center | top-right | middle-left | center | middle-right | bottom-left | bottom-center | bottom-right`

## 测试
```bash
pytest -q
```

## 目录结构
```
src/photowatermark/        # 核心代码
tests/                     # 单元测试
examples/quick_start.py    # 快速开始示例
```

## 已实现 PRD 2.1 核心功能
- 路径输入与验证
- EXIF 日期提取
- 水印配置
- 水印绘制与保存

## 后续可扩展
- 无 EXIF 时回退文件时间
- 处理统计与日志
- GUI 界面 / Web 界面

---
MIT License
