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
直接在项目根目录：
```python
from photowatermark.scanner import scan_directory
from photowatermark.exif_reader import extract_date
from photowatermark.watermark_config import WatermarkConfig
from photowatermark.watermarker import apply_watermark

scan_res = scan_directory('./photos')
out_dir = scan_res.root / f"{scan_res.root.name}_watermark"
for img in scan_res.images:
	exif_res = extract_date(img)
	date_text = exif_res.date_text
	if not date_text:
		# 回退：文件修改时间
		from datetime import datetime
		date_text = datetime.fromtimestamp(img.stat().st_mtime).strftime('%Y-%m-%d')
	cfg = WatermarkConfig(text=date_text, position='bottom-right')
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
examples/images/           # 示例图片目录（自备图片）
photowatermark.py          # 运行入口 (python photowatermark.py ...)
```

## 已实现 PRD 2.1 核心功能
- 路径输入与验证
- EXIF 日期提取
- 水印配置
- 水印绘制与保存

## 回退逻辑说明
当图片缺少 EXIF 拍摄时间时，自动使用文件修改时间（本地时间）作为水印日期。

## 后续可扩展
- 增加统计：EXIF 成功/文件时间回退数量
- 增加日志输出 / JSON 报告
- GUI / Web 界面

---
MIT License
