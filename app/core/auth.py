from fastapi import Header, HTTPException
import jwt

from app.core.settings import JWT_SECRET, JWT_ISSUER

def require_auth(authorization: str | None = Header(default=None)):
    if not JWT_SECRET:
        raise HTTPException(status_code=500, detail="JWT_SECRET not configured")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            options={"require": ["exp", "iss"]},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
