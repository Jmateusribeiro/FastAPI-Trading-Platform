"""
Main module defining a FastAPI application
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from trading_api.routers import orders

API_DESCRIPTION = """
A RESTful API designed to simulate a Forex trading platform for creating, retrieving, and deleting orders.
When an order is created, it is initially assigned the status "pending". 
Over time, the order's status is automatically and randomly updated to either "executed" or "canceled", reflecting the dynamic nature of real-world trading.
"""

app = FastAPI(
    title="Forex Trading Platform API",
    description=API_DESCRIPTION,
    version="0.0.1"
)

app.include_router(orders.router)
add_pagination(app)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Exception handler for validation errors.

    :param request: The incoming request
    :param exc: The instance of RequestValidationError
    :return: JSONResponse with HTTP 400 status code and error details
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# Health check endpoint for API
@app.get('/health', include_in_schema=False)
def health() -> int:
    """
    Health check endpoint.

    :return: HTTP 200 status code indicating API health
    """
    return 200
