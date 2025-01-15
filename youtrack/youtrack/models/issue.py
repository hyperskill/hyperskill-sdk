from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from youtrack.youtrack.models.common import MillisecondsDatetime
    from youtrack.youtrack.models.user import YouTrackUser


class YouTrackCustomField(BaseModel):
    name: str
    value: (
        str
        | int
        | dict[str, object]
        | list[dict[str, object]]
        | MillisecondsDatetime
        | YouTrackUser
        | list[YouTrackUser]
        | None
    ) = None

    model_config = ConfigDict(populate_by_name=True)


class YouTrackIssue(BaseModel):
    id_readable: str = Field(alias="idReadable")
    summary: str
    created: MillisecondsDatetime
    updated: MillisecondsDatetime
    custom_fields: list[YouTrackCustomField] = Field(alias="customFields")
