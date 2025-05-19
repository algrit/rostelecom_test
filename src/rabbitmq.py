from typing import Annotated

from aio_pika import Channel
from fastapi import Depends, Request


async def get_rabbit_channel(request: Request) -> Channel:
    return request.app.state.rmq_channel


RMQChannelDep = Annotated[Channel, Depends(get_rabbit_channel)]
