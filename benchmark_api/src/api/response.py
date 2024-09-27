import json
from fastapi.responses import JSONResponse
from typing import Any, Mapping
from starlette.background import BackgroundTask


class APIResponse(JSONResponse):

    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        """
        Initializes an APIResponse object.

        Args:
            content (Any): The content of the response.
            status_code (int, optional): The HTTP status code of the response. Defaults to 200.
            headers (Mapping[str, str] | None, optional): The headers of the response. Defaults to None.
            media_type (str | None, optional): The media type of the response. Defaults to None.
            background (BackgroundTask | None, optional): The background task of the response. Defaults to None.

        Returns:
            None
        """
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        """
        Renders the API response content into bytes.

        Args:
            content (Any): The content of the response.

        Returns:
            bytes: The rendered response content in bytes.
        """
        is_successful = self.status_code < 400

        res_content = {
            "success": is_successful,
            "data": content if is_successful else None,
            "message": content if not is_successful else None,
        }

        return json.dumps(
            res_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
