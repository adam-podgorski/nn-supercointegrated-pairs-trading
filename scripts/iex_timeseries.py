from datetime import datetime
from iexfinance.stocks import get_historical_data
import os
import pandas as pd
import pickle
from time import sleep

# Import symbols
df = pd.read_csv('data/snp100.csv')

# IEX Authentication
os.environ['IEX_API_VERSION'] = "iexcloud-sandbox"
real_token = os.environ['IEX_TOKEN']
test_token = os.environ['IEX_TEST_TOKEN']
os.environ['IEX_TOKEN'] = test_token

# Set up variables
start = datetime(2017, 1, 1)
end = datetime(2019, 11, 22)

def csv_fn(fund_type):
    return 'data/snp{}.csv'.format(fund_type)

def create_df(fund_type):
    return pd.read_csv(csv_fn(fund_type))

def symbols(fund_type):
    df = create_df(fund_type)    
    return df.Symbols.to_list()

def pickle_fn(fund_type):
    return 'data/snp{}_test_data.pickle'.format(fund_type)

def save_test_data(fund_type):
    snp_test_data = [
        get_historical_data(
            symbol, 
            start, 
            end, 
            output_format='pandas'
            ) \
                for symbol in symbols(fund_type) if sleep(0.2) is None
        ]
    pickle.dump(snp_test_data, open(pickle_fn(fund_type), 'wb'))

def load_test_data(fund_type):
    symbol_list = symbols(fund_type)
    data_load = pickle.load(open(pickle_fn(fund_type), 'rb'))
    return dict(zip(symbol_list, data_load))

os.environ['IEX_TOKEN'] = real_token