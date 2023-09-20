import logging
from core import *
from cred import *
from datetime import datetime
import time

QTY = 15 #Nifty Lot Size = 50, Banknifty= 15
SL = 50  #Points

# Configure logging
logging.basicConfig(filename='my_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    logging.info(current_time)

    start_time = '18:01'
    end_time = '20:30'

    api = ShoonyaApiPy()

    try:
        login = login_to_api(api, user, pwd, totp_key, app_key, imei)
        if login:
            logging.info(f'Successfully Logged In Welcome {user}')
        else:
            logging.error('Login Failed')
    except Exception as e:
        logging.error(f'Login Failed: {e}')

    symbol, index = get_live_index_info()
    index_ltp = get_live_index_price(api, symbol)
    logging.info(f'Current LTP of {index} {index_ltp}')

    if index == 'NIFTY':
        strike = get_strike(float(index_ltp))
    else:
        strike = get_strike_banknifty(float(index_ltp))
    logging.info(f'Current Strike Price {strike}')

    ce_token, pe_token, ce_tysm, pe_tysm = get_atm_strike_token_data(api, index, strike)
    logging.info(f'Ce Token {ce_token}, Ce TYSM {ce_tysm}')
    logging.info(f'Pe Token {pe_token}, Pe TYSM {pe_tysm}')

    option_price_ce = get_option_price(api, ce_token)
    option_price_pe = get_option_price(api, pe_token)
    logging.info(f'Current Price for CE {option_price_ce} and for PE {option_price_pe}')

    while current_time < start_time:
        time_left = (datetime.strptime(start_time, "%H:%M") - datetime.strptime(current_time, "%H:%M")).total_seconds() / 60
        logging.info(f'Waiting for {time_left} minutes before execution')
        time.sleep(2)
        now = datetime.now()
        current_time = now.strftime("%H:%M")

    while start_time <= current_time <= end_time:
        #Straddle Placed
        ce_order_details, pe_order_details = place_strangles(QTY, api, ce_tysm, pe_tysm, index)
        logging.info(f'Straddle Order Placed Details: CE {ce_order_details}, PE {pe_order_details}')

        #Check Straddle Order Status and Average Price
        ce_order_status, ce_avg_price = check_order_status(api, ce_order_details)
        pe_order_status, pe_avg_price = check_order_status(api, pe_order_details)
        logging.info(f'Order Status Main Staddle Ce {ce_order_status} And Average Price {ce_avg_price}')
        logging.info(f'Order Status of Main Straddle Pe {pe_order_status} And Average Price {pe_avg_price}')

        #Break the Code If the Staddle Did Not Placed Or Have Any Error
        if pe_order_status and ce_order_status != 'COMPLETE':
            raise TypeError('Main Straddle Order Did Not Execute Check Manually')

        #Stoploss CE Order Placed
        if ce_order_status == 'REJECTED':
            ce_stoploss = place_stoploss(api, float(ce_avg_price) + SL, ce_tysm, QTY)
            logging.info(f'CE Stoploss Placed Successfully, CE Stoploss Details {ce_stoploss}')
        else:
            logging.info('Orders CE Side Rejected')


        #Stoploss PE Order Placed
        if pe_order_status == 'COMPLETE':
            pe_stoploss = place_stoploss(api, float(pe_avg_price) + SL, pe_tysm, QTY)
            logging.info(f'PE Stoploss Placed Successfully, PE Stoploss Details {pe_stoploss}')                   
        else:
            logging.info('Order PE Side Rejected')

        

        try:
            # Check Ce stoploss Order Status details
            ce_stoploss_details, ce_stoploss_avg = check_order_status(api, ce_stoploss)
            logging.info(f'Ce Stoploss Order Status {ce_stoploss_details} And Average Price of the CE Stoploss {ce_stoploss_avg}')
        except Exception as e:
            logging.info(f'Order Status Checking for Stoploss CE Side Failed {e}')

        try:
            # Check pe stoploss details
            pe_stoploss_details, pe_stoploss_avg = check_order_status(api, pe_stoploss)
            logging.info(f'Pe Stoploss Order Status {pe_stoploss_details} And Average Price of the PE Stoploss {pe_stoploss_avg}')
        except Exception as e:
            logging.info(f'Order Status Checking for Stoploss PE Side Failed {e}')

        if ce_stoploss_details and pe_stoploss_details == 'COMPLETE':
            logging.info('Everything Placed Successfully Active Monitoring Now')
            print('Everything Done Start Monitoring Now')

        break

if __name__ == "__main__":
    main()
