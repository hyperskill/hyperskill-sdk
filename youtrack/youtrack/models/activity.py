from __future__ import annotations

from pydantic import BaseModel, Field

from youtrack.models.common import MillisecondsDatetime  # noqa: TC001


class YouTrackActivityItem(BaseModel):
    id: str
    timestamp: MillisecondsDatetime | None = None
    target_member: str | None = Field(alias="targetMember", default=None)
    added: object | None = None
