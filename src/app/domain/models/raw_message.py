from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RawMessage(BaseModel):
    source_type: str
    source_name: str
    algorithm_type: str
    parser_type: str
    payload: str
    received_at: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)
