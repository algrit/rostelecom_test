import uuid
from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from aio_pika import Message

from src.rabbitmq import RMQChannelDep
from .schemas import *


class TaskStatus(str, Enum):
    PENDING = "Task is still running"
    COMPLETED = "Completed"


in_memory_db: list[dict[str, str]] = []

router = APIRouter(
    prefix="/cpe",
    tags=["Сервис 'B' решающий задачу асинхронного запуска процесса конфигурации"],
)


@router.post("/{id}", summary="Endpoint для конфигурации конкретного устройства")
async def params_input(id: str, cpe_data: ParamsInput, channel: RMQChannelDep):
    try:
        task_data = ParamsBase(id=id, **cpe_data.model_dump())
    except ValidationError:
        raise HTTPException(404, "The requested equipment is not found")
    if not channel:
        raise HTTPException(500, "Internal provisioning exception")

    task_id = str(uuid.uuid4())
    try:
        await channel.default_exchange.publish(
            Message(
                body=task_data.model_dump_json().encode(),
                message_id=task_id,
                correlation_id=task_id,
                reply_to="task_status_queue",
            ),
            timeout=60,
            routing_key="conf_task_queue",
        )
    except Exception:
        raise HTTPException(500, "Internal provisioning exception")

    in_memory_db.append(
        {"task_id": task_id, "device_id": id, "status": TaskStatus.PENDING}
    )
    return {"task_id": task_id}


@router.get(
    "/{id}/task/{task}", summary="Endpoint для проверки статуса задачи конфигурации"
)
async def params_check(id: str, task: str, channel: RMQChannelDep):
    my_task_lst = [t for t in in_memory_db if t["task_id"] == task]
    if not my_task_lst:
        raise HTTPException(404, "The requested task is not found")
    my_task = my_task_lst[0]
    if my_task["device_id"] != id:
        raise HTTPException(404, "The requested equipment is not found")
    if my_task["status"] == TaskStatus.COMPLETED:
        return {"message": my_task["status"]}

    task_status_queue = await channel.get_queue("task_status_queue")
    try:
        async with task_status_queue.iterator() as queue_iter:
            async for message in queue_iter:
                if message.message_id == task:
                    my_task["status"] = TaskStatus.COMPLETED
                    await message.ack()
                    return {"message": my_task["status"]}
    except Exception:
        raise HTTPException(500, "Internal provisioning exception")

    return {"message": my_task["status"]}
