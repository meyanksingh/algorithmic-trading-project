from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import math
from datetime import datetime
import calendar
import time
import pandas as pd
import datetime as dt

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/')


def login_to_api(api, user, pwd, totp_key, app_key, imei):
    try:
        api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(
            totp_key).now(), vendor_code=user+'_U', api_secret=app_key, imei=imei)
        return True
    except Exception as e:
        print(f'Login Failed: {e}')
        return False


def get_live_index_info():
    current_date = dt.date.today()
    current_day = current_date.strftime('%A')

    symbol = "26000" if current_day == "Thursday" else '26009'
    index = 'NIFTY' if current_day == "Thursday" else 'BANKNIFTY'

    return symbol, index


def get_live_index_price(api, symbol):
    try:
        data = api.get_quotes('NSE', symbol)
        index_ltp = data['lp']
        return index_ltp
    except Exception as e:
        print(f"Error getting live index price for {symbol}: {e}")
        return None


def get_strike_banknifty(index_ltp):
    try:
        index_ltp = float(index_ltp)
        mod = int(index_ltp) % 100
        return int(math.floor(index_ltp / 100)) * 100 if mod < 50 else int(math.ceil(index_ltp / 100)) * 100
    except ValueError as e:
        print(f"Error converting index_ltp to float: {e}")
        return None


def get_strike(indextp):
    mod = int(indextp) % 50
    if mod < 25:
        atmStrike = int(math.floor(indextp / 50)) * 50
    else:
        atmStrike = int(math.ceil(indextp / 50)) * 50
    return atmStrike



def get_atm_strike_token_data(api,index,strike):
    cm = datetime.now().month
    fm = calendar.month_name[cm]
    month = fm[:3]
    ce_txt = f'{index} {month} {strike} CE'
    pe_txt = f'{index} {month} {strike} PE'
    ce_tysm,ce_token = get_symbol_token(api, 'NFO', ce_txt)
    pe_tysm,pe_token = get_symbol_token(api, 'NFO', pe_txt)
    return pe_token,ce_token,ce_tysm,pe_tysm

def get_symbol_token(api, exchange, symbol):
    try:
        res = api.searchscrip(exchange, symbol)
        df = pd.DataFrame(res['values'])
        trading_symbol = df['tsym'].iloc[0]
        tokens = (df['token'].iloc[0])
        return trading_symbol,tokens
    except Exception as e:
        print(f"Error getting token for {symbol}: {e}")
        return None



def get_option_price(api, token):
    try:
        ret = api.get_quotes('NFO', token)
        return ret['lp']
    except Exception as e:
        print(f"Error getting price for token {token}: {e}")
        return None



def place_strangles(qty, api, trading_symbolCE, trading_symbolPE, index):
    if index == 'NIFTY' and qty % 50 != 0:
        raise ValueError("Quantity should be divisible by 50 only.")

    try:
        ret1 = api.place_order(buy_or_sell='S', product_type='I',
                               exchange='NFO', tradingsymbol=trading_symbolCE,
                               quantity=qty, discloseqty=0, price_type='MKT', price=0.00, trigger_price=0.00,
                               retention='DAY', remarks='my_order_001')
        print(f'Order Placed for CE Side with the order number {ret1["norenordno"]} And The Current Status is {ret1["stat"]}')
    except Exception as e:
        print('Order Placing for CE Side Failed')
        ret1 = None

    try:
        ret2 = api.place_order(buy_or_sell='S', product_type='I',
                               exchange='NFO', tradingsymbol=trading_symbolPE,
                               quantity=qty, discloseqty=0, price_type='MKT', price=0.00, trigger_price=0.00,
                               retention='DAY', remarks='my_order_001')
        print(f'Order Placed for PE Side with the order number {ret2["norenordno"]} And The Current Status is {ret2["stat"]}')
    except Exception as e:
        print('Order Placing for PE Side Failed')
        ret2 = None
    return ret1["norenordno"], ret2["norenordno"]


def check_order_status(api,orderno):
    try:
        ret = api.single_order_history(orderno=orderno)
        

    except Exception as e:
        print('Error Check the Status of the Order',e)
    return ret[0]['status'], ret[0]['prc']


def place_stoploss(api,sl_price,tysm,qty):
    ret = api.place_order(buy_or_sell='B', product_type='I',
                        exchange='NFO', tradingsymbol=tysm, 
                        quantity=qty, discloseqty=0,price_type='SL-LMT', price=sl_price, trigger_price=sl_price-2,
                        retention='DAY', remarks='my_order_001')
    print(f'Order Successfully Placed for {tysm}  with the order number {ret["norenordno"]} And The Current Status is {ret["stat"]}')                   
    return ret["norenordno"]


