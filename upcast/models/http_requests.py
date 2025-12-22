"""Data models for HTTP request scanner."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class HttpRequestUsage(BaseModel):
    """A single HTTP request usage.

    Attributes:
        location: Location in 'file:line' format
        statement: Request statement
        method: HTTP method (GET, POST, etc.)
        params: Query parameters
        headers: Request headers
        json_body: JSON request body
        data: Form data
        timeout: Request timeout
        session_based: Whether using requests.Session
        is_async: Whether using async library
    """

    location: str = Field(..., description="file:line format")
    statement: str = Field(..., description="Request statement")
    method: str = Field(..., description="HTTP method")
    params: dict[str, Any] | None = Field(None, description="Query parameters")
    headers: dict[str, Any] | None = Field(None, description="Request headers")
    json_body: dict[str, Any] | None = Field(None, description="JSON body")
    data: Any | None = Field(None, description="Form data")
    timeout: float | int | None = Field(None, description="Timeout")
    session_based: bool = Field(default=False, description="Using session")
    is_async: bool = Field(default=False, description="Async request")


class HttpRequestInfo(BaseModel):
    """Information about HTTP requests to a URL.

    Attributes:
        method: Primary HTTP method
        library: Primary library (requests, httpx, aiohttp, urllib)
        usages: List of request usages
    """

    method: str = Field(..., description="Primary HTTP method")
    library: str = Field(..., description="Primary library (requests, httpx, etc)")
    usages: list[HttpRequestUsage] = Field(..., description="Request usages")


class HttpRequestSummary(ScannerSummary):
    """Summary statistics for HTTP requests.

    Attributes:
        total_requests: Total number of requests
        unique_urls: Number of unique URLs
        by_library: Count by library
    """

    total_requests: int = Field(ge=0, description="Total number of requests")
    unique_urls: int = Field(ge=0, description="Number of unique URLs")
    by_library: dict[str, int] = Field(default_factory=dict, description="Count by library")


class HttpRequestOutput(ScannerOutput[dict[str, HttpRequestInfo]]):
    """Complete output from HTTP request scanner.

    Attributes:
        summary: Summary statistics
        results: HTTP requests keyed by URL
    """

    summary: HttpRequestSummary
    results: dict[str, HttpRequestInfo] = Field(..., description="HTTP requests")
