from fastapi import Response
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str

def error_response(error: str, status_code: int):
    """
    Create an error response with the given error message and status code.

    Args:
    error (str): The error message.
    status_code (int): The status code.

    Returns:
    Response: The error response.
    """
    if error is None:
        error = "An unknown error occurred"
    error_response = ErrorResponse(error=error)
    return Response(error_response.json(), status_code=status_code)

class SuccessResponse(BaseModel):
    message: str

def success_response(message: str, status_code: int):
    """
    Create a success response with the given message and status code.

    Args:
    message (str): The success message.
    status_code (int): The status code.

    Returns:
    Response: The success response.
    """
    success_response = SuccessResponse(message=message)
    return Response(success_response.json(), status_code=status_code)