from core.constant import FUTURES, PERPETUAL, SPOT

BinancePoint = {
    'rest': {
        'address': 'https://api.binance.com',
        'sandbox': 'https://testnet.binance.vision',
        'route': {
            'instruments': '/api/v3/exchangeInfo',
            'l2book': '/api/v3/depth?symbol={}&limit={}',
            'authentication': '/api/v3/userDataStream',
        },
    },
}

OKXPoint = {
    'rest': {
        'address': 'https://www.okx.com',
        'route': {
            'instruments': [
                '/api/v5/public/instruments?instType=SPOT',
                '/api/v5/public/instruments?instType=SWAP',
                '/api/v5/public/instruments?instType=FUTURES',
            ],
            'liquidations': '/api/v5/public/liquidation-orders?instType={}&limit=100&state={}&uly={}'
        }
    }
}

BinanceFuturesPoint = {
    'rest': {
        'address': 'https://fapi.binance.com',
        'sandbox': 'https://testnet.binancefuture.com',
        'route': {
            'instruments': '/fapi/v1/exchangeInfo',
            'l2book': '/fapi/v1/depth?symbol={}&limit={}',
            'authentication': '/fapi/v1/listenKey',
            'open_interest': '/fapi/v1/openInterest?symbol={}',
        }
    },
}

BinanceDeliveryPoint = {
    'rest': {
        'address': 'https://dapi.binance.com',
        'sandbox': 'https://testnet.binancefuture.com',
        'route': {
            'instruments': '/dapi/v1/exchangeInfo',
            'l2book': '/dapi/v1/depth?symbol={}&limit={}',
            'authentication': '/dapi/v1/listenKey',
            'open_interest': '/dapi/v1/openInterest?symbol={}',
        }
    },
}

BinanceRestPoint = {
    'BinanceRest': {
        'api': 'https://api.binance.com/api/v3/'
    },
    'BinanceFutures': {
        'api': 'https://fapi.binance.com/fapi/v1/'
    },
    'BinanceDelivery': {
        'api': 'https://dapi.binance.com/dapi/v1/'
    },
    'BinanceUSRest': {
        'api': 'https://api.binance.us/api/v3/'
    },
    'BinanceTRRest': {
        'api': 'https://api.binance.me/api/v3/'
    },
    'OKXCoin': {
        'api': 'https://www.okx.com',
    }
}

OKXRestPoint = {
    'OKXCoin': {
        'api': 'https://www.okx.com/',
    }
}
