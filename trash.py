def _4_perf_ranks(df_close, days_lookbacks, verbose=False):
    """Returns perf_ranks_dict(dic. of dic. of symbols ranked in descending performance)
     and ranked_perf_ranks_dict(dic. of symbols ranked in descending frequency in a combined
     pool of symbols in perf_ranks_dict). 

    Args:
        df_close(dataframe): dataframe of symbols' close with
         DatetimeIndex e.g. (['2016-12-19', ... '2016-12-22']), symbols as 
         column names, and symbols' close as column values.
        days_lookbacks(list of negative integers): list of number of days to lookback,
         e.g. [-15, -30] 

    Return:
        perf_ranks_dict({dic): dic. of dic. of symbols ranked in descending performance.
         First dic keys are: 'period' + str(days_lookbacks[0]), ... ,  'period' + str(days_lookbacks[-1])
         Second dic keys are: 'r_CAGR/UI', 'r_CAGR/Std' and 'r_Std/UI'
         e.g.:
          {
            period-15': {
                         'r_CAGR/UI':  ['HZNP', ... , 'CB'],
                         'r_CAGR/Std': ['BBW', ... , 'CPRX'],
                         'r_Std/UI':   ['ENR', ... , 'HSY']
                        },
            ... ,
            'period-60': {
                          'r_CAGR/UI':  ['WNC', ... , 'FSLR'],
                          'r_CAGR/Std': ['VCYT', ... , 'BERY'],
                          'r_Std/UI':   ['MYOV', ... , 'NSC']
                         }
          }
        ranked_perf_ranks_dict(dic): dic. of symbols ranked in descending frequency in a combined
         pool of symbols in perf_ranks_dict.  Key is 'ranked_perf_ranks_period' + str(days_lookbacks)  
         e.g.: 
          {'ranked_perf_ranks_period[-15, -30]': ['HZNP', ... , 'NSC']}
    """

    # from myUtils import pickle_load, pickle_dump, symb_perf_stats_vectorized
    from myUtils import symb_perf_stats_vectorized    

    perf_ranks_dict = {}  # dic of performance ranks
    syms_perf_rank = []  # list of lists to store top 100 ranked symbols

    # days_lookbacks = [-15, -30, -60, -120, -240]
    # days_lookbacks = [-15, -30]

    for days_lookback in days_lookbacks:
        f_name = 'period' + str(days_lookback)
        _df_c = df_close[days_lookback::]
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

    # pickle_dump(perf_ranks_dict, path_data_dump, f_pickled_perf_ranks_dict)
    # print(f'perf_ranks_dict:\n{perf_ranks_dict}\n')

    syms_perf_rank  # list of lists of top 100 rank
    l_syms_perf_rank = [val for sublist in syms_perf_rank for val in sublist]  # flatten list of lists

    from collections import Counter
    cnt_symbol_freq = Counter(l_syms_perf_rank)  # count symbols and frequency
    # print(cnt_symbol_freq) 
    l_tuples = cnt_symbol_freq.most_common()  # convert to e.g [('AKRO', 6), ('IMVT', 4), ... ('ADEA', 3)]
    symbols_ranked_perf_ranks = [symbol for symbol, count in l_tuples]  # select just the symbols without the frequency counts
    symbols_ranked_perf_ranks  # list of most common symbols in syms_perf_rank in descending order

    ranked_perf_ranks_dict ={}
    # f_name = f'ranked_perf_ranks_period' + str(_periods)  # key name, ranked_perf_ranks_dict
    f_name = f'ranked_perf_ranks_period' + str(days_lookbacks)  # key name, ranked_perf_ranks_dict
    ranked_perf_ranks_dict[f'{f_name}'] = symbols_ranked_perf_ranks # values: list of most common symbols in all performance ranks in descending order
    # pickle_dump(ranked_perf_ranks_dict, path_data_dump, f_pickled_ranked_perf_ranks_dict)
    # print(f'ranked_perf_ranks_dict:\n{ranked_perf_ranks_dict}\n')

    return perf_ranks_dict, ranked_perf_ranks_dict

