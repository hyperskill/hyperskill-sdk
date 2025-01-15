from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from youtrack.models.common import MillisecondsDatetime  # noqa: TC001


class YouTrackCustomField(BaseModel):
    name: str
    value: str | int | dict[str, object] | list[dict[str, object]] | None = None

    model_config = ConfigDict(populate_by_name=True)


class YouTrackIssue(BaseModel):
    id: str
    id_readable: str | None = Field(alias="idReadable", default=None)
    summary: str | None = None
    created: MillisecondsDatetime | None = None
    updated: MillisecondsDatetime | None = None
    custom_fields: list[YouTrackCustomField] = Field(alias="customFields", default_factory=list)

    @property
    def assignee_id(self) -> str | None:
        """Get assignee id from issue."""
        assignee_field = next((cf for cf in self.custom_fields if cf.name == "Assignee"), None)
        if not assignee_field or not assignee_field.value:
            msg = "Assignee field is empty"
            raise ValueError(msg)
        return str(assignee_field.value)
