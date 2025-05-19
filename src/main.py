from contextlib import asynccontextmanager

import logging

import sys
from pathlib import Path


import aio_pika
import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))


from config import settings

from api import router as v1_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info("FastAPI trying to connect to RabbitMQ")
    rmq_connection = await aio_pika.connect_robust(settings.get_rmq_dsn)
    rmq_channel = await rmq_connection.channel()
    await rmq_channel.declare_queue("conf_task_queue")
    await rmq_channel.declare_queue("task_status_queue")
    app.state.rmq_channel = rmq_channel
    logging.info("Created connection: %s", rmq_connection)
    yield
    await rmq_channel.close()
    await rmq_connection.close()


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)
