from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sea_routes.exceptions import RouteNotFoundException
from sea_routes.router import sea_routes_router

app = FastAPI()
app.include_router(sea_routes_router)


@app.exception_handler(RouteNotFoundException)
async def route_not_found_exception_handler(
    request: Request, exception: RouteNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"message": exception.message},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred.",
            "details": str(exc),
        },
    )
