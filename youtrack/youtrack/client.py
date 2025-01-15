from __future__ import annotations

import http
from typing import TYPE_CHECKING

import httpx
import structlog
from httpx import Response

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = structlog.get_logger()


class YouTrackClient:
    """Implementation of YouTrack API."""

    def __init__(self, youtrack_token: str, youtrack_api_url: str) -> None:
        """Initialize YouTrack API client."""
        self._token = youtrack_token
        self._api_url = youtrack_api_url
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }

    def get_issues(self, query: str, fields: Iterable[str]) -> list[dict[str, object]]:
        """Get issues from YouTrack by query."""
        params = {
            "query": query,
            "fields": ",".join(fields),
        }
        response = self.get("issues", params)
        return response.json() if response and response.status_code == http.HTTPStatus.OK else []

    def get_issue_comments(self, issue_id: str) -> list[dict[str, object]]:
        """Get comments for an issue."""
        response = self.get(f"issues/{issue_id}/comments")
        return response.json() if response and response.status_code == http.HTTPStatus.OK else []

    def get_user(self, user_id: str) -> dict[str, object]:
        """Get user information from YouTrack.

        Args:
            user_id: ID of the user.

        Returns:
            Dictionary containing user information.
        """
        response = self.get(f"users/{user_id}")
        return response.json() if response and response.status_code == http.HTTPStatus.OK else {}

    def get(self, endpoint: str, params: dict[str, str] | None = None) -> Response | None:
        """Send request to YouTrack API."""
        try:
            response = httpx.get(
                f"{self._api_url}/{endpoint}", headers=self._headers, params=params
            )
            response.raise_for_status()
        except httpx.RequestError:
            logger.exception("Error making request to YouTrack API")
            return None
        else:
            return response
