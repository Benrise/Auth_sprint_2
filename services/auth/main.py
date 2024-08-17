import logging
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, status
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

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider        
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)
    await FastAPILimiter.init(redis.redis)
    if settings.debug:
        from db.postgres import create_database
        await create_database()
    configure_tracer()
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


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(
        resource=Resource.create({SERVICE_NAME: "auth-service"})
    ))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='jaeger',
                agent_port=6831,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(users.router, prefix='/auth/api/v1/users', tags=['users'], dependencies=[Depends(get_current_user_global)])
app.include_router(roles.router, prefix='/auth/api/v1/roles', tags=['roles'], dependencies=[Depends(get_current_user_global)])

FastAPIInstrumentor.instrument_app(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
