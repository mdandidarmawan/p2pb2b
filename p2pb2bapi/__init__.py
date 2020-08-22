import requests
import json
import base64
import hmac
import hashlib
import time


class P2PB2B:
    BASE_URL = 'https://p2pb2b.io'
    API_V1_URL = '/api/v1'
    METHODS = {
        'markets': '/public/markets',
        'tickers': '/public/tickers',
        'ticker': '/public/ticker',
        'book': '/public/book',
        'history': '/public/history',
        'history_result': '/public/history/result',
        'products': '/public/products',
        'symbols': '/public/symbols',
        'depth': '/public/depth/result',
        'new_order': '/order/new',
        'cancel_order': '/order/cancel',
        'orders': '/orders',
        'balances': '/account/balances',
        'balance': '/account/balance',
        'order': '/account/order',
        'order_history': '/account/order_history'
    }

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.encode()

    ################################################
    #
    # PUBLIC API
    #
    ################################################

    def get_markets(self):
        return self._get_request(self.METHODS['markets'])

    def get_tickers(self):
        return self._get_request(self.METHODS['tickers'])

    def get_ticker(self, market):
        params = {'market': market}
        return self._get_request(self.METHODS['ticker'], params)

    def get_book(self, market, side, offset=0, limit=50):
        params = {
            'market': market,
            'side': side,
            'offset': offset,
            'limit': limit
        }
        return self._get_request(self.METHODS['book'], params)

    def get_history(self, market, last_id, limit=50):
        params = {
            'market': market,
            'last_id': last_id,
            'limit': limit
        }
        return self._get_request(self.METHODS['history'], params)

    def get_history_result(self, market, since, limit=50):
        params = {
            'market': market,
            'since': since,
            'limit': limit
        }
        return self._get_request(self.METHODS['history_result'], params)

    def get_products(self):
        return self._get_request(self.METHODS['products'])

    def get_symbols(self):
        return self._get_request(self.METHODS['symbols'])

    def get_depth(self, market, limit=50):
        params = {
            'market': market,
            'limit': limit
        }
        return self._get_request(self.METHODS['depth'], params)

    ################################################
    #
    # MARKET API
    #
    ################################################

    def new_order(self, market, side, amount, price):
        data = {
            'market': market,
            'side': side,
            'amount': amount,
            'price': price
        }
        return self._post_request(self.METHODS['new_order'], data)

    def cancel_order(self, market, order_id):
        data = {
            'market': market,
            'order_id': order_id
        }
        return self._post_request(self.METHODS['cancel_order'], data)

    def get_orders(self, market, offset=0, limit=50):
        data = {
            'market': market,
            'offset': offset,
            'limit': limit,
        }
        return self._post_request(self.METHODS['orders'], data)

    ################################################
    #
    # ACCOUNT API
    #
    ################################################

    def get_balances(self):
        return self._post_request(self.METHODS['balances'])

    def get_balance(self, currency):
        data = {'currency': currency}
        return self._post_request(self.METHODS['balance'], data)

    def get_order(self, order_id, offset=0, limit=50):
        data = {
            'order_id': order_id,
            'offset': offset,
            'limit': limit
        }
        return self._post_request(self.METHODS['order'], data)

    def get_order_history(self, offset=0, limit=50):
        data = {
            'offset': offset,
            'limit': limit
        }
        return self._post_request(self.METHODS['order_history'], data)

    ################################################
    #
    # CALLS TO P2PB2B
    #
    ################################################

    def _get_request(self, request_url, params=None):
        response = requests.get(
            url=self.BASE_URL + self.API_V1_URL + request_url,
            params=params
        )
        return response.json()

    def _post_request(self, request_url, data=None):
        timestamp = str(time.time()).split('.')[0]
        base_data = {
            'request': self.API_V1_URL + request_url,
            'nonce': timestamp
        }
        if data is not None:
            data.update(base_data)
        else:
            data = base_data
        data = json.dumps(data, separators=(',', ':'))
        payload = base64.b64encode(data.encode())
        signature = hmac.new(self.api_secret, payload,
                             hashlib.sha512).hexdigest()
        payload = payload.decode()
        headers = {
            'Content-type': 'application/json',
            'X-TXC-APIKEY': self.api_key,
            'X-TXC-PAYLOAD': payload,
            'X-TXC-SIGNATURE': signature
        }
        response = requests.post(
            url=self.BASE_URL + self.API_V1_URL + request_url,
            data=data,
            headers=headers
        )
        return response.json()
