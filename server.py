from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from clients import connections
from db import get_api
import threading
from loger.loger import *


app = FastAPI()


class RequestData(BaseModel):
    user_id: int


# asincio
async def async_wrapper(api_key, secret_key):
    from stream import main
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, main, api_key, secret_key)
    except Exception as e:
        log_warning(e)


# threading
async def process_data_thread(api_key, api_secret):
    from stream import main
    threading.Thread(target=main, args=(api_key, api_secret)).start()


@app.post("/process_data")
async def process_data(request_data: RequestData):
    # Получаем данные из запроса
    user_id = request_data.user_id

    if user_id not in connections:

        # Получаем API по user_id
        api_key, api_secret = get_api(user_id)

        log_info('-------Connecting the client-------')

        # Соханение user_id
        connections.append(user_id)  # Заменить на что то другое

        # Запускаем обработку через threading
        # await process_data_thread(api_key_t, sicret_key_t)

        # Запускаем обработку данных асинхронно
        asyncio.create_task(async_wrapper(api_key, api_secret))

        return {"message": "Данные обработаны и успешно отправлены"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
