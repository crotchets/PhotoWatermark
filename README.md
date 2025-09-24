# PhotoWatermark

基于 EXIF 拍摄日期的批量图片文字水印工具。

## 功能特性
- 批量扫描目录图片（支持 JPG/JPEG/PNG/TIFF 等）
- 提取 EXIF DateTimeOriginal 并格式化为 `YYYY-MM-DD`
- 可配置：字体大小、颜色、透明度、九宫格位置、偏移、自动缩放、描边
- 输出到 `<原目录名>_watermark` 子目录，保持原文件名
- CLI 或 Python 代码方式调用

## 安装 / 使用准备
项目采用 src 目录结构，`photowatermark` 包位于 `src/photowatermark/` 下。要在未打包安装的情况下运行 CLI，有三种方式：

1) 直接使用提供的便捷入口脚本 `photowatermark.py`（推荐本地快速试用）。
2) 临时把 `src` 加入环境变量 `PYTHONPATH` 后再使用 `python -m photowatermark.cli`。
3) 以开发模式安装（生成可直接 `python -m photowatermark.cli` 的环境）。

安装依赖：
```bash
pip install -r requirements.txt
```

可选（开发模式安装包，后续可直接 import 或调用）：
```bash
pip install -e .  # 若根目录后续补充 pyproject.toml/setup.cfg 可使用
```

## 命令行使用
### 方式 A：便捷入口脚本（无需设置 PYTHONPATH）
```bash
python photowatermark.py \
	--input ./photos \
	--font-size 48 \
	--color 255,255,255 \
	--position bottom-right \
	--opacity 80 \
	--stroke-width 2 \
	--stroke-color 0,0,0
```

### 方式 B：手动添加 src 到路径后用模块形式
POSIX (bash/zsh)：
```bash
export PYTHONPATH=src
python -m photowatermark.cli -i ./photos
```

Windows PowerShell：
```powershell
$env:PYTHONPATH = "src"
python -m photowatermark.cli -i .\photos
```

### 方式 C：若已安装为包（例如未来提供 pyproject 并执行 `pip install -e .`）
```bash
python -m photowatermark.cli -i ./photos
```

Dry-run 查看扫描结果：
```bash
python photowatermark.py -i ./photos --dry-run
```

递归处理子目录：
```bash
python photowatermark.py -i ./photos --recursive
```

## Python 编程方式示例
直接在项目根目录（方式 A/B 未安装包时，需确保运行前已使用脚本或设置 PYTHONPATH）：
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

## 目录结构（节选）
```
src/photowatermark/        # 核心代码（包根）
	cli.py                   # CLI 入口 (python -m photowatermark.cli) - 需确保 src 在 PYTHONPATH
	scanner.py               # 扫描目录
	exif_reader.py           # EXIF 读取
	watermarker.py           # 水印绘制
photowatermark.py          # 便捷运行入口 (自动把 src 加入 sys.path)
examples/                  # 示例图片
tests/                     # 单元测试
```

运行选择说明：
- 临时试用：`python photowatermark.py -i <目录>`
- 保持模块风格：设置 `PYTHONPATH=src` 后 `python -m photowatermark.cli -i <目录>`
- 真正分发：补充打包配置后 `pip install -e .` 再直接模块方式。

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
