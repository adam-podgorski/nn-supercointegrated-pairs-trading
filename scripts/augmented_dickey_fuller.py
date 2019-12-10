import statsmodels.api as sm
import chart_studio
import chart_studio.plotly as py
import os
import pandas as pd
import plotly.figure_factory as ff

chart_studio.tools.set_credentials_file(
    username=os.environ['PLOTLY_USERNAME'], 
    api_key=os.environ['PLOTLY_API_KEY']
)

from scripts.iex_timeseries import symbols, load_test_data
n_symbols = 100
fund_type = str(n_symbols)
symbol_list = symbols(fund_type)
iex_data = load_test_data(fund_type)

def df_for_ols(pair):
    symbol1, symbol2 = pair
    df = pd.DataFrame()
    df['y'] = iex_data[symbol1].close.to_list()
    df['beta'] = iex_data[symbol2].close.to_list()
    df['alpha'] = 1
    return df    

def ADFTest(pair):
    subdf = df_for_ols(pair)
    regression = sm.OLS(
        endog=subdf['y'], 
        exog=subdf[['alpha', 'beta']], 
        missing='drop'
    )
    results = regression.fit()
    alpha_pos, beta_pos = [(param > 0) for param in results.params]
    return (alpha_pos and beta_pos)

df_jh = pd.read_pickle('data/johansen_100.pickle')
table_jh = ff.create_table(df_jh[['Pair', 'pValue']])
py.iplot(table_jh)
pairs = df_jh.Pairs.to_list()
df_jh['ADFPassed'] = [ADFTest(pair) for pair in pairs]
adf_fn = 'data/post_adf_100.pickle'
df_jh.to_pickle(adf_fn)
