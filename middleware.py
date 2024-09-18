from settings import get_settings
from security import check_token_valid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],  # Adjust to only allow specific origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=["Authorization"],  # Expose all headers
    )
    
    @app.middleware("http")
    async def check_token(request:Request, call_next):
        token = request.headers.get("Authorization")
        if token is None:
            return JSONResponse(content={"detail":"Token is missing"}, status_code=401)
        
        try:
            check_token_valid(token)
        except HTTPException as e:
            return JSONResponse(content={"detail":str(e.detail)}, status_code=e.status_code)
        
        response = await call_next(request)
        return response