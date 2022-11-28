perf_ranks_dict = {}  # dic of performance ranks
syms_perf_rank = []  # list of lists to store top 100 ranked symbols
days_lookbacks = [-15, -30, -60, -120, -240]
for days_lookback in days_lookbacks:
  f_name = 'period' + str(days_lookback)

  _df_c = df_c[days_lookback::]
  symbols, period_yr, drawdown, UI, max_drawdown, returns_std, Std_UI, CAGR, CAGR_Std, CAGR_UI = \
      symb_perf_stats_vectorized(_df_c)
  caches_perf_stats_vect = []
  for symbol in symbols:
      date_first = drawdown.index[0].strftime('%Y-%m-%d')
      date_last = drawdown.index[-1].strftime('%Y-%m-%d')
      cache = (symbol, date_first, date_last, period_yr, CAGR[symbol],
              UI[symbol], Std_UI[symbol], CAGR_Std[symbol], CAGR_UI[symbol])
      # append performance data (tuple) to caches_perf_stats (list)
      caches_perf_stats_vect.append(cache)
  column_names = ['symbol', 'first date', 'last date', 'Year', 'CAGR',
                  'UI', 'Std/UI', 'CAGR/Std', 'CAGR/UI']

  # write symbols' performance stats to dataframe
  df_ps = pd.DataFrame(caches_perf_stats_vect, columns=column_names)
  df_ps['r_CAGR/UI'] = df_ps['CAGR/UI'].rank(ascending=False)
  df_ps['r_CAGR/Std'] = df_ps['CAGR/Std'].rank(ascending=False)
  df_ps['r_Std/UI'] = df_ps['Std/UI'].rank(ascending=False)
  
  _dict = {}
  cols_sort = ['r_CAGR/UI', 'r_CAGR/Std', 'r_Std/UI']
  # print(f'{f_name} top 100 symbols')  
  for col in cols_sort:
    symbols_top_100 = df_ps.sort_values(by=[col]).head(100).symbol.values
    syms_perf_rank.append(list(symbols_top_100))
    # print(f'{col}: {symbols_top_100}')
    _dict[col] = symbols_top_100
    perf_ranks_dict[f'{f_name}'] = _dict
  # print(' ')

pickle_dump(perf_ranks_dict, path_data_dump, f_pickled_perf_ranks_dict)
print(f'perf_ranks_dict:\n{perf_ranks_dict}\n')