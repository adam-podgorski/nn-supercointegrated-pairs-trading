# Some imports to make tables and graphs interactive and pretty.
import chart_studio
import chart_studio.plotly as py
import os
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

chart_studio.tools.set_credentials_file(
    username=os.environ['PLOTLY_USERNAME'], 
    api_key=os.environ['PLOTLY_API_KEY']
)

import numpy as np
from statsmodels.tsa.vector_ar.vecm import coint_johansen

class JohansenResults:
    def __init__(self, timeseries, det_order=0, lagged_terms=14):
        timeseries = np.array(timeseries)
        try:
            result = coint_johansen(timeseries, det_order, lagged_terms)
        except np.linalg.LinAlgError as error:
            raise error
        self.rank_pi = np.linalg.matrix_rank(np.array(result.cvt))
        self.trace_stat = np.array(result.lr1)
        self.trace_stat_crit_vals = np.array(result.cvt)[:,2]
        self.max_eig_stat = np.array(result.lr2)
        self.max_eig_stat_crit_vals = np.array(result.cvm)[:,2]
        self.eigenvalues = np.array(result.eig)
        self.pi = np.array(result.evec)
        self.output = [
            self.trace_stat,
            self.trace_stat_crit_vals,
            self.max_eig_stat,
            self.max_eig_stat_crit_vals
        ]
        self.is_pair = None
        self.p_val = None
        self.pair_test()

    def pair_test(self):
        self.is_pair = None
        r_max = len(self.trace_stat) - 1
        stat = [
            self.trace_stat[r_max], 
            self.max_eig_stat[r_max]
            ]
        crit_val = [
            self.trace_stat_crit_vals[r_max], 
            self.max_eig_stat_crit_vals[r_max]
            ]
        test = [(stat[i] > crit_val[i]) for i in range(2)]

        if all(test):
            self.is_pair = 1
            self.p_val = np.max(stat)


from scripts.iex_timeseries import symbols, load_test_data
n_symbols = 100
fund_type = str(n_symbols)
symbol_list = symbols(fund_type)
iex_data = load_test_data(fund_type)


times = iex_data[symbol_list[0]].index
close_dfs = pd.DataFrame(index=times)
close_dfs.dropna(inplace=True)
for symb in symbol_list:
    df = iex_data[symb]
    try:
        close_dfs[symb] = iex_data[symb].close
    except KeyError:
        continue
    except AttributeError:
        continue
close_dfs.to_numpy().shape


pairs_df = pd.DataFrame()
pairs = []
evecs = []
eigvals = []
pvals = []


johansen_pair_matrix = np.ones((n_symbols, n_symbols))
johansen_pair_matrix[:] = None

for i in range(n_symbols):
    symbol = symbol_list[i]
    for j in range(i+1, n_symbols):
        next_symbol = symbol_list[j]

        try:
            ts = close_dfs[[symbol, next_symbol]].to_numpy()
        except KeyError:
            pass

        try:
            jh = JohansenResults(ts)
        except np.linalg.LinAlgError:
            continue

        johansen_pair_matrix[i, j] = jh.is_pair

        if jh.is_pair is not None:
            pairs.append((symbol, next_symbol))
            evecs.append(jh.pi)
            eigvals.append(jh.eigenvalues)
            pvals.append(jh.p_val)


output_df = pd.DataFrame(index=range(len(pairs)))
output_df['Pair'] = pairs
output_df['Eigenvectors'] = evecs
output_df['Eigenvalues'] = eigvals
output_df['pValue'] = pvals
output_df.to_pickle('data/johansen_{}.pickle'.format(fund_type))


fig = go.Figure(data=go.Heatmap(
                    z=johansen_pair_matrix,
                    x=symbol_list,
                    y=symbol_list))
fig.show()

