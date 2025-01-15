from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import structlog
from httpx import Response

from youtrack.youtrack.models.activity import YouTrackActivityItem
from youtrack.youtrack.models.comment import YouTrackComment
from youtrack.youtrack.models.issue import YouTrackIssue
from youtrack.youtrack.models.user import YouTrackUser

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = structlog.get_logger()


class YouTrackClient:
    """Implementation of YouTrack API."""

    def __init__(self, youtrack_api_url: str, youtrack_token: str) -> None:
        """Initialize YouTrack API client."""
        self._api_url = youtrack_api_url
        self._token = youtrack_token
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }

    def get_issues(self, query: str, fields: Iterable[str]) -> tuple[YouTrackIssue, ...]:
        """Get issues from YouTrack by query."""
        params = {
            "query": query,
            "fields": ",".join(fields),
        }
        response = self.get("issues", params)
        response.raise_for_status()

        return tuple(YouTrackIssue(**issue) for issue in response.json())

    def get_issue_comments(self, issue_id: str) -> tuple[YouTrackComment, ...]:
        """Get comments for an issue."""
        response = self.get(f"issues/{issue_id}/comments")
        response.raise_for_status()
        return tuple(YouTrackComment(**comment) for comment in response.json())

    def get_user(self, user_id: str) -> YouTrackUser:
        """Get user information from YouTrack.

        Args:
            user_id: ID of the user.

        Returns:
            Dictionary containing user information.
        """
        response = self.get(f"users/{user_id}")
        response.raise_for_status()
        return YouTrackUser(**response.json())

    def get_activities(
        self, issue_id: str, categories: Iterable[str], fields: Iterable[str]
    ) -> tuple[YouTrackActivityItem, ...]:
        """Get activities for an issue."""
        url = f"issues/{issue_id}/activities"
        params = {
            "categories": ",".join(categories),
            "fields": ",".join(fields),
        }
        response = self.get(url, params=params)
        response.raise_for_status()
        return tuple(YouTrackActivityItem(**activity) for activity in response.json())

    def get(self, endpoint: str, params: dict[str, str] | None = None) -> Response:
        """Send request to YouTrack API."""
        response = httpx.get(f"{self._api_url}/{endpoint}", headers=self._headers, params=params)
        response.raise_for_status()
        return response
