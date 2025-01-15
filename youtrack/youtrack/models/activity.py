from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from youtrack.youtrack.models.common import MillisecondsDatetime


class YouTrackActivityItem(BaseModel):
    id: str
    timestamp: MillisecondsDatetime | None = None
