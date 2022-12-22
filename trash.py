
def _4_perf_ranks(df_close, days_lookbacks, verbose=False):
    """Returns perf_ranks_dict(dic. of dic. of symbols ranked in descending
     performance) and ranked_perf_ranks_dict(dic. of symbols ranked in
     descending frequency in a combined pool of symbols in perf_ranks_dict).

    Args:
        df_close(dataframe): dataframe of symbols' close with
         DatetimeIndex e.g. (['2016-12-19', ... '2016-12-22']), symbols as
         column names, and symbols' close as column values.
        days_lookbacks(list of positive integers): list of number of days to
        look-back, e.g. [15, 30], for performance calculation.

    Return:
        perf_ranks_dict({dic): dic. of dic. of symbols ranked in descending
         performance.
         First dic keys are:
          'period' + str(days_lookbacks[0]), ... ,
          'period' + str(days_lookbacks[-1])
         Second dic keys are:
          'r_CAGR/UI', 'r_CAGR/retnStd' and 'r_retnStd/UI'
         e.g.:
          {
            period-15': {
                         'r_CAGR/UI':  ['HZNP', ... , 'CB'],
                         'r_CAGR/retnStd': ['BBW', ... , 'CPRX'],
                         'r_retnStd/UI':   ['ENR', ... , 'HSY']
                        },
            ... ,
            'period-60': {
                          'r_CAGR/UI':  ['WNC', ... , 'FSLR'],
                          'r_CAGR/retnStd': ['VCYT', ... , 'BERY'],
                          'r_retnStd/UI':   ['MYOV', ... , 'NSC']
                         }
          }
        ranked_perf_ranks_dict(dic): dic. of symbols ranked in descending
         frequency in a combined pool of symbols in perf_ranks_dict.  Key is
         'ranked_perf_ranks_period' + str(days_lookbacks), e.g.:
         {'ranked_perf_ranks_period[-15, -30]': ['HZNP', ... , 'NSC']}
    """

    import pandas as pd
    from myUtils import symb_perf_stats_vectorized_v2

    perf_ranks_dict = {}  # dic of performance ranks
    syms_perf_rank = []  # list of lists to store top 100 ranked symbols

    for days_lookback in days_lookbacks:
        days_lookback = -1 * days_lookback
        f_name = "period" + str(days_lookback)
        _df_c = df_close[days_lookback::]
        (
            symbols,
            period_yr,
            drawdown,
            UI,
            max_drawdown,
            retnStd,
            retnStd_d_UI,
            CAGR,
            CAGR_d_retnStd,
            CAGR_d_UI,        
        ) = symb_perf_stats_vectorized_v2(_df_c)            


        caches_perf_stats_vect = []
        for symbol in symbols:
            date_first = drawdown.index[0].strftime("%Y-%m-%d")
            date_last = drawdown.index[-1].strftime("%Y-%m-%d")
            cache = (
                symbol,
                date_first,
                date_last,
                period_yr,
                CAGR[symbol],
                UI[symbol],
                retnStd_d_UI[symbol],
                CAGR_d_retnStd[symbol],
                CAGR_d_UI[symbol],
            )
            # append performance data (tuple) to caches_perf_stats (list)
            caches_perf_stats_vect.append(cache)
        column_names = [
            "symbol",
            "first date",
            "last date",
            "Year",
            "CAGR",
            "UI",
            "retnStd/UI",
            "CAGR/retnStd",
            "CAGR/UI",
        ]

        # write symbols' performance stats to dataframe
        df_ps = pd.DataFrame(caches_perf_stats_vect, columns=column_names)
        df_ps["r_CAGR/UI"] = df_ps["CAGR/UI"].rank(ascending=False)
        df_ps["r_CAGR/retnStd"] = df_ps["CAGR/retnStd"].rank(ascending=False)
        df_ps["r_retnStd/UI"] = df_ps["retnStd/UI"].rank(ascending=False)

        _dict = {}
        cols_sort = ["r_CAGR/UI", "r_CAGR/retnStd", "r_retnStd/UI"]

        # print(f'{f_name} top 100 symbols')
        for col in cols_sort:
            symbols_top_n = (

                # df_ps.sort_values(by=[col]).head(n_symbols).symbol.values
                df_ps.sort_values(by=[col]).symbol.values

            )
            syms_perf_rank.append(list(symbols_top_n))
            # print(f'{col}: {symbols_top_n}')
            _dict[col] = symbols_top_n
            perf_ranks_dict[f"{f_name}"] = _dict

    syms_perf_rank  # list of lists of top 100 rank
    l_syms_perf_rank = [
        val for sublist in syms_perf_rank for val in sublist
    ]  # flatten list of lists

    from collections import Counter

    cnt_symbol_freq = Counter(l_syms_perf_rank)  # count symbols and frequency
    # print(cnt_symbol_freq)
    l_tuples = (
        cnt_symbol_freq.most_common()
    )  # convert to e.g [('AKRO', 6), ('IMVT', 4), ... ('ADEA', 3)]
    symbols_ranked_perf_ranks = [
        symbol for symbol, count in l_tuples
    ]  # select just the symbols without the frequency counts

    ranked_perf_ranks_dict = {}
    f_name = f"ranked_perf_ranks_period" + str(
        days_lookbacks
    )  # key name, ranked_perf_ranks_dict
    ranked_perf_ranks_dict[
        f"{f_name}"
    # values: list of most common symbols in all performance ranks in
    #  descending order
    ] = symbols_ranked_perf_ranks

    return perf_ranks_dict, ranked_perf_ranks_dict
