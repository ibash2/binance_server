from binance_server.get_client import get_spot_client

def get_listen_key(api_key, secret_key):
   return get_spot_client(api_key, secret_key).new_listen_key().get('listenKey')
