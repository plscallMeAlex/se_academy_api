from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

# Program health check
@app.get("/")
def status_check():
    try:
        return JSONResponse(content={"status" :"ok"})
    except Exception as e:
        return JSONResponse(content={"status" :"error"})