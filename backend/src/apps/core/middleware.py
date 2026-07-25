from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.core.config import settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging with request_id and environment headers."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=str(request.url.query),
            client_ip=request.client.host if request.client else None,
        )

        response = await call_next(request)

        # Inject response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Environment"] = settings.APP_ENV
        response.headers["X-API-Version"] = settings.API_VERSION

        logger.info(
            "Request completed",
            request_id=request_id,
            status_code=response.status_code,
        )

        return response
