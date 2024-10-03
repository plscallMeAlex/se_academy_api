from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from middleware import add_middleware
from security import check_token_valid
from routers.routes import router as api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(api_router)

# add middleware
origins = ["http://localhost", "http://127.0.0.1", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],
    expose_headers=["Authorization"],
)

app.mount(
    "/images",
    StaticFiles(directory="images"),
    name="images",
)


# @app.middleware("http")
# async def check_token(request: Request, call_next):
#     # Will delete the path docs and openapi later
#     if (
#         (request.url.path == "/" and request.method == "GET")
#         or (request.url.path == "/user/login")
#         or (request.url.path == "/user/register")
#         or (request.url.path == "/docs" and request.method == "GET")
#         or (request.url.path == "/openapi.json" and request.method == "GET")
#     ):
#         response = await call_next(request)
#         return response

#     token = request.headers.get("Authorization")

#     if token is None:
#         return JSONResponse(
#             content={"success": False, "error_msg": "Token is missing"},
#             status_code=401,
#         )

#     try:
#         check_token_valid(token)
#     except HTTPException as e:
#         return JSONResponse(
#             content={"success": False, "error_mg": str(e.detail)},
#             status_code=e.status_code,
#         )

#     response = await call_next(request)
#     return response


# add_middleware(app)


# custom exception handler
@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"success": False, "error_msg": exc.detail}, status_code=exc.status_code
    )


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"success": False, "error_msg": "Internal Server Error"},
        status_code=500,
    )


# Program health check
@app.get("/")
def status_check():
    try:
        return JSONResponse(content={"status": True})
    except Exception as e:
        return JSONResponse(content={"status": False, "error_msg": str(e)})
