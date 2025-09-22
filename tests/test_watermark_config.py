import pytest
from photowatermark.watermark_config import WatermarkConfig


def test_watermark_config_ok():
    cfg = WatermarkConfig(text='2024-01-01', font_size=40, color=(10,20,30), opacity=50, position='center')
    assert cfg.text == '2024-01-01'
    assert cfg.font_size == 40
    assert cfg.opacity == 50
    assert cfg.position == 'center'


def test_watermark_config_invalid_font():
    with pytest.raises(ValueError):
        WatermarkConfig(text='x', font_size=5)


def test_watermark_config_invalid_opacity():
    with pytest.raises(ValueError):
        WatermarkConfig(text='x', opacity=101)


def test_watermark_config_invalid_position():
    with pytest.raises(ValueError):
        WatermarkConfig(text='x', position='no-place')


def test_watermark_config_invalid_color():
    with pytest.raises(ValueError):
        WatermarkConfig(text='x', color=(256, 0, 0))
