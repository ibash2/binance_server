from time import sleep
import requests
import click
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance_server.get_client import get_spot_client
from binance_server.get_listen_key import get_listen_key
from binance_server.update_listen_key import update_listen_key
import asyncio
from loger.loger import *
import json


# Функция-обработчик для обработки входящих сообщений от вебсокета
def on_message_ws(_, message):
    r = json.loads(message)
    if "e" in r:
        if r["e"] == "executionReport":
            # Отправка данных на API методом post
            try:
                requests.post("http://localhost:1234/orders", data=message)
            except Exception as e:
                log_warning('message send error')
                print(e)

    else:
        print("Подписка user_data")


# Функция-обработчик для обработки ошибок вебсокета
def on_error(_, error):
    log_warning(error)


# Функция-обработчик для обработки закрытия вебсокета
def on_close_ws(_):
    log_info("closed")


# Функция-обработчик для установления соединения с вебсокетом
def on_open_ws(_):
    log_info("connecting")


def main(api_key, secret_key):
    # ************ Запуск сокета ************
    click.secho("Поднимаю Stream", fg='magenta')

    # Тестовая сеть
    # client = SpotWebsocketStreamClient(
    #     stream_url="wss://testnet.binance.vision", on_message=on_message_ws)

    # Рабочая сеть
    client = SpotWebsocketStreamClient(
        on_open=on_open_ws,
        on_message=on_message_ws,
        on_error=on_error,
        on_close=on_close_ws)

    try:
        # Рабочий листенкей
        listen_key = get_listen_key(api_key=api_key, secret_key=secret_key)

        client.user_data(listen_key=listen_key, id=1)

        # Обновление listen_key каждый час
        i = 1
        while i < 3700:
            if i % 3500 == 0:
                update_listen_key(
                    api_key=api_key,
                    secret_key=secret_key,
                    listen_key=listen_key
                )
                log_info("ListenKey обновлён")
                i = 0 

            if i % 60 == 0 and i != 0:
                click.secho(f"Сокет ок, {int(i/60)} мин.", fg="yellow")
            i += 1
            sleep(1)

    except KeyboardInterrupt:
        ...
    finally:
        client.stop()
