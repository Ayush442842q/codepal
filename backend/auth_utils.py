import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

# Define the secret key for JWT token creation and verification
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise Exception("SECRET_KEY environment variable is not set")

class TokenPayload(BaseModel):
    user_id: int
    username: str

def create_token(payload: TokenPayload):
    """
    Create a JWT token with the given payload.

    Args:
    payload (TokenPayload): The payload to include in the token.

    Returns:
    str: The created JWT token.
    """
    if SECRET_KEY is None:
        raise Exception("SECRET_KEY environment variable is not set")
    return jwt.encode(payload.dict(), SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    """
    Verify a JWT token and extract its payload.

    Args:
    token (str): The token to verify.

    Returns:
    TokenPayload: The payload extracted from the token.

    Raises:
    HTTPException: If the token is invalid or has expired.
    """
    if SECRET_KEY is None:
        raise Exception("SECRET_KEY environment variable is not set")
    if token is None:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to verify token") from e

# Define the authentication scheme for FastAPI
auth_scheme = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials):
    """
    Get the current user from the authentication token.

    Args:
    token (HTTPAuthorizationCredentials): The authentication token.

    Returns:
    TokenPayload: The payload extracted from the token.

    Raises:
    HTTPException: If the token is invalid or has expired.
    """
    if SECRET_KEY is None:
        raise Exception("SECRET_KEY environment variable is not set")
    try:
        return verify_token(token.credentials)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get current user") from e