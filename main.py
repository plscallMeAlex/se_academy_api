from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPExceptions
from middleware import add_middleware
from routers.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

# add middleware
add_middleware(app)

# custom exception handler
@app.exception_handler(Exception)
async def custom_exception_handler(request:Request, exc:StarletteHTTPExceptions):
    return JSONResponse(content={"success":False,"error_msg":str(exc)}, status_code=exc.status_code)

# Program health check
@app.get("/")
def status_check():
    try:
        return JSONResponse(content={"status" :True})
    except Exception as e:
        return JSONResponse(content={"status" :False, "error_msg":str(e)})