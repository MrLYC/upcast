"""Export and formatting functions for HTTP request data."""

from upcast.http_request_scanner.request_parser import HttpRequest


def format_request_output(requests_by_url: dict[str, list[HttpRequest]], summary: dict) -> dict:
    """Format HTTP requests for YAML/JSON output.

    Args:
        requests_by_url: Dictionary mapping URLs to requests
        summary: Summary statistics

    Returns:
        Formatted dictionary ready for export
    """
    output = {"summary": summary}

    # Sort URLs alphabetically
    for url in sorted(requests_by_url.keys()):
        requests = requests_by_url[url]

        # Determine primary method and library (most common)
        methods = [req.method for req in requests]
        libraries = [req.library for req in requests]
        primary_method = max(set(methods), key=methods.count)
        primary_library = max(set(libraries), key=libraries.count)

        # Sort usages by location
        sorted_requests = sorted(requests, key=lambda r: r.location)

        output[url] = {
            "method": primary_method,
            "library": primary_library,
            "usages": [format_single_usage(req) for req in sorted_requests],
        }

    return output


def format_single_usage(request: HttpRequest) -> dict:
    """Format a single HTTP request usage.

    Args:
        request: HttpRequest object

    Returns:
        Formatted usage dictionary
    """
    return {
        "location": request.location,
        "statement": request.statement,
        "method": request.method,
        "params": request.params,
        "headers": request.headers,
        "json_body": request.json_body,
        "data": request.data,
        "timeout": request.timeout,
        "session_based": request.session_based,
        "is_async": request.is_async,
    }
