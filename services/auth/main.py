import logging
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from async_fastapi_jwt_auth.exceptions import AuthJWTException

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from api.v1 import users, roles
from api.v1.user_auth import get_current_user_global

from core.config import settings
from core.logger import LOGGING
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)
    await FastAPILimiter.init(redis.redis)
    if settings.debug:
        from db.postgres import create_database
        await create_database()
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    default_response_class=ORJSONResponse,
    docs_url="/auth/api/v1/docs",
    openapi_url="/auth/api/v1/docs.json",
    lifespan=lifespan,
    dependencies=[Depends(RateLimiter(times=5, seconds=10))],
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    return await call_next(request)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

app.include_router(users.router, prefix='/auth/api/v1/users', tags=['users'], dependencies=[Depends(get_current_user_global)])
app.include_router(roles.router, prefix='/auth/api/v1/roles', tags=['roles'], dependencies=[Depends(get_current_user_global)])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
