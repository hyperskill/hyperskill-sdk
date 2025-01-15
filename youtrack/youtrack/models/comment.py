from __future__ import annotations

from pydantic import BaseModel


class YouTrackComment(BaseModel):
    id: str
