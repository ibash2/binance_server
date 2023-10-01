from binance.spot import Spot


def get_spot_client(api_key, secret_key):
    """
    Функция для инициализации спотового клиента
    для Тестнета binance
    :return:
    """
    return Spot(
        # base_url='https://testnet.binance.vision',
        api_key=api_key,
        api_secret=secret_key,
    )
