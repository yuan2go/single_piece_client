from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


class BaseAlgorithmSettings(BaseModel):
    algorithm_type: str
    algorithm_name: str
    parser_type: str
    render_format: Literal['json', 'toml', 'yaml'] = 'json'
    config_output_dir: Path
    result_schema: str = 'default'
    extra: dict[str, Any] = Field(default_factory=dict)


class DefaultAlgorithmSettings(BaseAlgorithmSettings):
    algorithm_type: str = 'default'
    algorithm_name: str = 'default_algorithm'
    parser_type: str = 'jsonl_default'
    config_output_dir: Path = Path('./runtime/default/config')
    threshold: float = 0.85
    speed: float = 1.0


class RoiAlgorithmSettings(BaseAlgorithmSettings):
    algorithm_type: str = 'roi'
    algorithm_name: str = 'roi_algorithm'
    parser_type: str = 'http_json_default'
    config_output_dir: Path = Path('./runtime/roi/config')
    roi_x: int = 0
    roi_y: int = 0
    roi_width: int = 100
    roi_height: int = 100
    model_path: str = './models/roi.bin'


AlgorithmSettings = DefaultAlgorithmSettings | RoiAlgorithmSettings
