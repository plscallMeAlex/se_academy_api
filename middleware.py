from settings import get_settings
from security import check_token_valid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()


def add_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust to only allow specific origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=["Authorization"],  # Expose all headers
    )

    # comment first to testing api
    @app.middleware("http")
    async def check_token(request: Request, call_next):
        # Will delete the path docs and openapi later
        if (
            (request.url.path == "/" and request.method == "GET")
            or (request.url.path == "/user/login")
            or (request.url.path == "/user/register")
            or (request.url.path == "/docs" and request.method == "GET")
            or (request.url.path == "/openapi.json" and request.method == "GET")
        ):
            response = await call_next(request)
            return response
        token = request.headers.get("Authorization")
        if token is None:
            return JSONResponse(
                content={"success": False, "error_msg": "Token is missing"},
                status_code=401,
            )

        try:
            check_token_valid(token)
        except HTTPException as e:
            return JSONResponse(
                content={"success": False, "error_mg": str(e.detail)},
                status_code=e.status_code,
            )

        response = await call_next(request)
        return response

    return app
