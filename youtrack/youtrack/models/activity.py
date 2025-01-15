from __future__ import annotations

from pydantic import BaseModel

from youtrack.models.common import MillisecondsDatetime  # noqa: TC001


class YouTrackActivityItem(BaseModel):
    id: str
    timestamp: MillisecondsDatetime | None = None
