from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from auth.utils import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.user = None
        request.state.authenticated = False

        token = request.cookies.get('session_token')
        if token:
            user = await get_current_user(token)
            if user:
                request.state.user = user
                request.state.authenticated = True

        return await call_next(request)
