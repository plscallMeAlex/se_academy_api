import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from middleware import add_middleware
from routers.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

# add middleware
add_middleware(app)


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
