from __future__ import annotations

from pydantic import BaseModel


class YouTrackUser(BaseModel):
    id: str | None = None
    name: str
    login: str
    email: str | None = None
