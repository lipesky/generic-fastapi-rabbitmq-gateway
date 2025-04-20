import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from patio import AsyncExecutor
from patio_rabbitmq import RabbitMQBroker
from src.settings import get_settings
# Support for cors
# from fastapi.middleware.cors import CORSMiddleware
from src.infra.rabbitmq.broker import broker, executor, rpc
# Just need to import here to make sure python process it and adds it to registry
from src.listener.listener import handler # setup listeners
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')


settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global broker, executor, rpc
    executor = AsyncExecutor(rpc, max_workers=16)
    app.state.executor = executor
    await executor.__aenter__()
    broker = RabbitMQBroker(
        executor, amqp_url=settings.rabbitmq_url, 
    )
    app.state.broker = broker
    await broker.__aenter__()
    print('🟢 RabbitMQBroker initialized')
    yield
    await broker.__aexit__(None, None, None)
    await executor.__aexit__(None, None, None)



app = FastAPI(
    title="Generic Service Consumer",
    lifespan=lifespan,
)

# app.include_router(
#     app_routes,
#     prefix='/api/v1/app',
#     tags=['app routes'],
# )

# Support for cors
# origins = [
#     "https://example.com.br",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get('/')
async def rootRoute():
    return Response('consumer-service', status_code=200)

@app.get('/healthcheck')
async def healthcheck():
    return Response(status_code=200)

if __name__ == '__main__':
    from uvicorn import run
    import os
    port = settings.port
    if not port:
        port = int(os.environ.get('PORT', '8000' if settings.environment == 'DEV' else '80'))
    run(
        'main:app',
        host='0.0.0.0',
        port=port,
        reload=settings.environment == 'DEV',
        root_path=settings.root_path,
    )