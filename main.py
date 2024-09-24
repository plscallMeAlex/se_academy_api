from fastapi import FastAPI
from fastapi.responses import JSONResponse
from middleware import add_middleware
from routers.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

# add middleware
add_middleware(app)

# Program health check
@app.get("/")
def status_check():
    try:
        return JSONResponse(content={"status" :True})
    except Exception as e:
        return JSONResponse(content={"status" :False, "error_msg":str(e)})