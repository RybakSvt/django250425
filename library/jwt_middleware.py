import time
from datetime import datetime, timezone
from typing import Callable, Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class JWTAuthMiddleware:
    refresh_window_seconds = 60

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def refresh_access_token(self, refresh_token: Optional[str]) -> Optional[str]:

        if not refresh_token:
            return None
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except TokenError:
            return None

    def _is_access_expiring(self, access_token_str: str) -> bool:
        try:
            token = AccessToken(access_token_str)
            exp_ts = int(token.get("exp"))
            now_ts = int(time.time())
            return exp_ts <= now_ts + self.refresh_window_seconds
        except Exception:
            return True

    def __call__(self, request: Request) -> Response:
        access_cookie = request.COOKIES.get("access_token")
        refresh_cookie = request.COOKIES.get("refresh_token")

        minted_access: Optional[str] = None
        access_expiry_dt: Optional[datetime] = None

        if access_cookie:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_cookie}"

            if self._is_access_expiring(access_cookie) and refresh_cookie:
                new_access = self.refresh_access_token(refresh_cookie)
                if new_access:
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                    minted_access = new_access
                    try:
                        exp_ts = AccessToken(new_access).get("exp")
                        access_expiry_dt = datetime.fromtimestamp(exp_ts, timezone.utc)
                    except Exception:
                        access_expiry_dt = None

        elif refresh_cookie:
            new_access = self.refresh_access_token(refresh_cookie)
            if new_access:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"
                minted_access = new_access
                try:
                    exp_ts = AccessToken(new_access).get("exp")
                    access_expiry_dt = datetime.fromtimestamp(exp_ts, timezone.utc)
                except Exception:
                    access_expiry_dt = None

        response = self.get_response(request)

        if minted_access:
            response.set_cookie(
                key="access_token",
                value=minted_access,
                httponly=True,
                secure=False,
                samesite="Lax",
                expires=access_expiry_dt,
                path="/",
            )

        return response
