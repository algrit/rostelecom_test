from functools import partial

from aio_pika import IncomingMessage, Message, RobustChannel, connect_robust
import asyncio


async def on_message(message: IncomingMessage, channel: RobustChannel):
    async with message.process():
        print(f"Получено сообщение: {message.body.decode()}")
        # Здесь логика конфигурации оборудования
        await asyncio.sleep(5)
        # Здесь процесс конфигурации оборудования завершен

        if message.reply_to:
            reply_status_message = Message(
                body=message.body, message_id=message.correlation_id
            )
            await channel.default_exchange.publish(
                reply_status_message, routing_key=message.reply_to
            )


async def main(port:int):
    consumer_rmq_connection = await connect_robust(f"amqp://guest:guest@localhost:{port}/")
    async with consumer_rmq_connection:
        consumer_rmq_channel = await consumer_rmq_connection.channel()
        queue = await consumer_rmq_channel.declare_queue("conf_task_queue")
        await queue.consume(partial(on_message, channel=consumer_rmq_channel))

        try:
            await asyncio.Future()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main(5672))
