def perf_eval(df_close):
  '''
  df_close is a dataframe with date index, columns of symbols' closing price, and symbol as column name.
  Calculate symbols' performance in drawdown, Ulcer-Index, max-drawdown, standard deviation of returns,
  standard deviation of returns / Ulcer-Index, CAGR, CAGR / standard deviation of returns, CAGR / Ulcer-Index.

  '''

#   from myUtils import symb_perf_stats_vectorized_v2
  from trash import symb_perf_stats_vectorized_v2  

  symbols, period_yr, drawdown, UI, max_drawdown, returns_std, returns_std_div_UI, CAGR, CAGR_div_returns_std, CAGR_div_UI = \
      symb_perf_stats_vectorized_v2(df_close)

  caches_perf_stats_vect = []
  for symbol in symbols:
      # date_first = drawdown.index[0].strftime('%Y-%m-%d')
      # date_last = drawdown.index[-1].strftime('%Y-%m-%d')
      date_first = df_close.index[0].strftime('%Y-%m-%d')
      date_last = df_close.index[-1].strftime('%Y-%m-%d')

      cache = (symbol, date_first, date_last, period_yr, CAGR[symbol],
              UI[symbol], returns_std_div_UI[symbol], CAGR_div_returns_std[symbol], CAGR_div_UI[symbol])
      # append performance data (tuple) to caches_perf_stats (list)
      caches_perf_stats_vect.append(cache)
  column_names = ['symbol', 'first date', 'last date', 'Year', 'CAGR',
                  'UI', 'return_std/UI', 'CAGR/return_std', 'CAGR/UI']
  # write symbols' performance stats to dataframe
  df_perf = pd.DataFrame(caches_perf_stats_vect, columns=column_names)

  _cols = ['CAGR', 'UI', 'retrun_std/UI', 'CAGR/return_std', 'CAGR/UI']
  grp_CAGR_d_UI_mean = df_perf['CAGR/UI'].mean()
  grp_CAGR_d_UI_std  = df_perf['CAGR/UI'].std()
  grp_CAGR_d_UI_mean_div_std = grp_CAGR_d_UI_mean / grp_CAGR_d_UI_std 

  grp_CAGR_d_retnStd_mean = df_perf['CAGR/return_std'].mean()
  grp_CAGR_d_retnStd_std = df_perf['CAGR/return_std'].std()
  grp_CAGR_d_retnStd_mean_div_std = grp_CAGR_d_retnStd_mean / grp_CAGR_d_retnStd_std

  grp_retnStd_d_UI_mean = df_perf['return_std/UI'].mean()
  grp_retnStd_d_UI_std = df_perf['return_std/UI'].std()
  grp_retnStd_d_UI_mean_div_std = grp_retnStd_d_UI_mean / grp_retnStd_d_UI_std

  return df_perf, grp_retnStd_d_UI_mean_div_std, grp_CAGR_d_retnStd_mean_div_std, grp_CAGR_d_UI_mean_div_std
