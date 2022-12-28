def _4_perf_ranks_2(df_close, n_top_syms=200, verbose=False):
    """Returns perf_ranks(dic. of dic. of symbols ranked in descending
     performance) and most_common_syms(list of tuples of the most common
     symbols in perf_ranks in descending frequency).
     Example of perf_ranks:
        {'period-120': {'r_CAGR/UI': array(['CDNA', 'AVEO', 'DVAX', 'XOMA',
         'BLFS'], dtype=object),
        'r_CAGR/retnStd': array(['CDNA', 'AVEO', 'CYRX', 'BLFS', 'XOMA'],
         dtype=object),
        'r_retnStd/UI': array(['GDOT', 'DVAX', 'XOMA', 'CTRA', 'FTSM'],
         dtype=object)}}
     Example of most_common_syms:
        [('XOMA', 3), ('CDNA', 2), ('AVEO', 2), ('DVAX', 2), ('BLFS', 2),
         ('CYRX', 1), ('GDOT', 1), ('CTRA', 1), ('FTSM', 1)]

    Args:
        df_close(dataframe): dataframe of symbols' close with
         DatetimeIndex e.g. (['2016-12-19', ... '2016-12-22']), symbols as
         column names, and symbols' close as column values.
        n_top_syms(int): number of top symbols to keep in perf_ranks

    Return:
        perf_ranks({dic): dic. of dic. of symbols ranked in descending
         performance.
         First dic key is: 'period-' + str(days_lookback)
         Second dic keys are:
          'r_CAGR/UI', 'r_CAGR/retnStd' and 'r_retnStd/UI'
         e.g.:
          {
            period-15': {
                         'r_CAGR/UI':  ['HZNP', ... , 'CB'],
                         'r_CAGR/retnStd': ['BBW', ... , 'CPRX'],
                         'r_retnStd/UI':   ['ENR', ... , 'HSY']
                        },

        most_common_syms(list of tuples): list of tuples of symbols:frequency
         in descending frequency count of symbols in perf_ranks.  Key is
         'ranked_perf_ranks_period-' + str(days_lookbacks), e.g.:
         {'ranked_perf_ranks_period-15': ['HZNP', ... , 'NSC']}
    """

    import pandas as pd
    from collections import Counter
    from myUtils import symb_perf_stats_vectorized_v2

    # dic of  dic of performance ranks
    # e.g. {'period-120': {'r_CAGR/UI': array(['LRN', 'APPS', 'FTSM', 'AU',
    #       'GRVY'], dtype=object),
    #      'r_CAGR/retnStd': array(['APPS', 'AU', 'LRN', 'GRVY', 'ERIE'],
    #       dtype=object),
    #      'r_retnStd/UI': array(['LRN', 'FTSM', 'AXSM', 'RCII', 'AU'],
    #       dtype=object)}}
    perf_ranks = {}
    syms_perf_rank = []  # list of lists to store top n ranked symbols

    days_lookback = len(df_close)
    f_name = "period-" + str(days_lookback)
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
    ) = symb_perf_stats_vectorized_v2(df_close)

    caches_perf_stats = []  # list of tuples in cache
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
        caches_perf_stats.append(cache)
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
    df_ps = pd.DataFrame(caches_perf_stats, columns=column_names)
    # create rank columns for performance stats
    df_ps["r_CAGR/UI"] = df_ps["CAGR/UI"].rank(ascending=False)
    df_ps["r_CAGR/retnStd"] = df_ps["CAGR/retnStd"].rank(ascending=False)
    df_ps["r_retnStd/UI"] = df_ps["retnStd/UI"].rank(ascending=False)

    _dict = {}
    cols_sort = ["r_CAGR/UI", "r_CAGR/retnStd", "r_retnStd/UI"]

    # print(f'{f_name} top 100 symbols')
    for col in cols_sort:
        symbols_top_n = (
            # sort df by column in col and return only the top symbols
            df_ps.sort_values(by=[col])
            .head(n_top_syms)
            .symbol.values
        )
        syms_perf_rank.append(list(symbols_top_n))
        _dict[col] = symbols_top_n
        perf_ranks[f"{f_name}"] = _dict

    syms_perf_rank  # list of lists of top n_top_syms symbols
    # flatten list of lists
    l_syms_perf_rank = [val for sublist in syms_perf_rank for val in sublist]

    cnt_symbol_freq = Counter(l_syms_perf_rank)  # count symbols and frequency
    # convert cnt_symbol_freq from counter obj. to list of tuples
    most_common_syms = (
        cnt_symbol_freq.most_common()
    )  # convert to e.g [('AKRO', 6), ('IMVT', 4), ... ('ADEA', 3)]

    return perf_ranks, most_common_syms

