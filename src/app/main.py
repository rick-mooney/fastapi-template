from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.requests import Request
import uvicorn

from app.api.v1.routers import (
    auth, generics
)

import app.config as config
import sentry_sdk

tags_metadata = [
    {"name": "Users", "description": "User APIs"},
]

app = FastAPI(
    description=f"API for {config.API_NAME} App",
    title=config.API_NAME,
    docs_url="/api/docs",
    openapi_url="/api",
    openapi_tags=tags_metadata,
    prefix="/api/v1",
    version="1.0",
    debug=config.ENVIRONMENT != 'production',
)

sentry_sdk.init(dsn=config.SENTRY_URL)

methods = ["GET", "POST", "DELETE", "PUT"]
headers = [
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Credentials",
    "Cookie",
    "Content-Type",
    "Host",
    "Location",
    "From",
    "Origin",
    "Referer",
    "Set-Cookie",
    "User-Agent",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_methods=methods,
    allow_credentials=True,
    allow_headers=headers,
)


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)
            sentry_sdk.capture_exception(e)
        raise e


@app.get("/api/v1")
async def root():
    # health check endpoint
    return {"message": "ok"}


# Routers - add custom routers before generics
app.include_router(auth.router, tags=["authentication"])
app.include_router(generics.router, tags=["REST API"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
