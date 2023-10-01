from binance_server.get_client import get_spot_client

def update_listen_key(api_key, secret_key, listen_key):
    get_spot_client(api_key, secret_key).renew_listen_key(listen_key)