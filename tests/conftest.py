import asyncio

import pytest
import aio_pika
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.main import app
from src.rabbitmq import get_rabbit_channel

from tests.mock_service_a import main

@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


async def test_rabbitmq_channel():
    rmq_connection = await aio_pika.connect_robust(settings.get_rmq_dsn)
    async with rmq_connection:
        rmq_channel = await rmq_connection.channel()
        yield rmq_channel


app.dependency_overrides[get_rabbit_channel] = test_rabbitmq_channel


@pytest.fixture(scope="session", autouse=True)
async def queues_setup(check_mode):
    async for channel in test_rabbitmq_channel():
        await channel.declare_queue("conf_task_queue")
        await channel.declare_queue("task_status_queue")


@pytest.fixture(scope="session", autouse=True)
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
