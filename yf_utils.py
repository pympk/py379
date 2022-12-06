def _2_split_train_val_test(
    df, s_train=0.7, s_val=0.2, s_test=0.1, verbose=False
):
    """Split df into training (df_train), validation (df_val)
        and test (df_test) and returns the splitted dfs

    Args:
        df(dataframe): dataframe to be splitted
        s_train(float): ratio of df_train / df, default = 0.7
        s_val(float): ratio of df_val / df, default = 0.2
        s_test(float): ratio of df_test / df, default = 0.1

    Return:
        df_train(dataframe): training portion of df
        df_val(dataframe): validation portion of df
        df_test(dataframe): test portion of df
    """

    if (s_train + s_val + s_test) - 1 > 0.0001:  # allow 0.01% error
        _sum = s_train + s_val + s_test
        raise Exception(
            f"s_train({s_train}) + s_val({s_val}) + s_test({s_test}) must sums to 1"
        )
    n_train = round(len(df) * s_train)
    n_val = round(len(df) * s_val)
    n_test = round(len(df) * s_test)
    df_train = df.iloc[0:n_train]
    df_val = df.iloc[n_train : (n_train + n_val)]
    df_test = df.iloc[(n_train + n_val) : :]

    len_df = len(df)
    len_train = len(df_train)
    len_val = len(df_val)
    len_test = len(df_test)
    sum_train_val_test = len_df + len_train + len_test

    if verbose:
        print(f"len(df): {len_df}")
        print(f"len(df_train): {len_train}")
        print(f"len(df_val): {len_val}")
        print(f"len(df_test): {len_test}")
        print(f"sum_train_val_test: {sum_train_val_test}")

    return df_train, df_val, df_test


def _3_random_slices(
    len_df, n_samples, days_lookback, days_eval, verbose=False
):
    """Returns a list of random tuples of start_train, end_train, end_eval, where
        iloc[start_train:end_train] is used for training, and iloc[end_train:end_eval]
        is used for evaluation.  The length of the list is equal to n_samples.
        i.e. [(248, 368, 388), (199, 319, 339), ... (45, 165, 185)]

    Args:
        len_df(int): length of dataframe
        n_samples(int): number of slices to return
        days_lookback(int):  number of days to lookback for training
        days_eval(int): number of days forward for evaluation

    Return:
        r_slices(list of tuples): list of random tuples of start_train, end_train, end_eval, where
          iloc[start_train:end_train] is used for training, and iloc[end_train:end_eval] is used for
          evaluation.
          i.e. [(248, 368, 388), (199, 319, 339), ... (45, 165, 185)]
    """

    import random
    from random import randint

    # random.seed(0)
    n_sample = 0
    days_total = days_lookback + days_eval
    if verbose:
        print(
            f"days_lookback: {days_lookback}, days_eval: {days_eval}, days_total: {days_total}, len_df: {len_df}"
        )

    if days_total > len_df:
        msg_err = f"days_total: {days_total} must be less or equal to len_df: {len_df}"
        raise SystemExit(msg_err)

    # random slices of iloc for train and eval that fits the days_lookback, days_eval and total len_df constraints
    r_slices = []
    while n_sample < n_samples:
        n_rand = randint(0, len_df)
        start_train = n_rand - days_lookback
        end_train = n_rand
        # start_eval = n_rand
        end_eval = n_rand + days_eval
        if 0 <= start_train and end_eval <= len_df:
            r_slices.append((start_train, end_train, end_eval))
            n_sample += 1

    return r_slices


def _4_perf_ranks(df_close, days_lookbacks, n_symbols=100, verbose=False):
    """Returns perf_ranks_dict(dic. of dic. of symbols ranked in descending performance)
     and ranked_perf_ranks_dict(dic. of symbols ranked in descending frequency in a combined
     pool of symbols in perf_ranks_dict).

    Args:
        df_close(dataframe): dataframe of symbols' close with
         DatetimeIndex e.g. (['2016-12-19', ... '2016-12-22']), symbols as
         column names, and symbols' close as column values.
        days_lookbacks(list of negative integers): list of number of days to look-back,
         e.g. [-15, -30]
        n_sysmbols(int): number of symbols to be returned, default=100

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
    import pandas as pd
    from myUtils import symb_perf_stats_vectorized

    perf_ranks_dict = {}  # dic of performance ranks
    syms_perf_rank = []  # list of lists to store top 100 ranked symbols

    # days_lookbacks = [-15, -30, -60, -120, -240]
    # days_lookbacks = [-15, -30]

    for days_lookback in days_lookbacks:
        f_name = "period" + str(days_lookback)
        _df_c = df_close[days_lookback::]
        (
            symbols,
            period_yr,
            drawdown,
            UI,
            max_drawdown,
            returns_std,
            Std_UI,
            CAGR,
            CAGR_Std,
            CAGR_UI,
        ) = symb_perf_stats_vectorized(_df_c)
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
                Std_UI[symbol],
                CAGR_Std[symbol],
                CAGR_UI[symbol],
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
            "Std/UI",
            "CAGR/Std",
            "CAGR/UI",
        ]

        # write symbols' performance stats to dataframe
        df_ps = pd.DataFrame(caches_perf_stats_vect, columns=column_names)
        df_ps["r_CAGR/UI"] = df_ps["CAGR/UI"].rank(ascending=False)
        df_ps["r_CAGR/Std"] = df_ps["CAGR/Std"].rank(ascending=False)
        df_ps["r_Std/UI"] = df_ps["Std/UI"].rank(ascending=False)

        _dict = {}
        cols_sort = ["r_CAGR/UI", "r_CAGR/Std", "r_Std/UI"]

        # print(f'{f_name} top 100 symbols')
        for col in cols_sort:
            symbols_top_n = (
                df_ps.sort_values(by=[col]).head(n_symbols).symbol.values
            )
            syms_perf_rank.append(list(symbols_top_n))
            # print(f'{col}: {symbols_top_n}')
            _dict[col] = symbols_top_n
            perf_ranks_dict[f"{f_name}"] = _dict
        # print(' ')

    # pickle_dump(perf_ranks_dict, path_data_dump, f_pickled_perf_ranks_dict)
    # print(f'perf_ranks_dict:\n{perf_ranks_dict}\n')

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
    symbols_ranked_perf_ranks = symbols_ranked_perf_ranks[:n_symbols]

    ranked_perf_ranks_dict = {}
    # f_name = f'ranked_perf_ranks_period' + str(_periods)  # key name, ranked_perf_ranks_dict
    f_name = f"ranked_perf_ranks_period" + str(
        days_lookbacks
    )  # key name, ranked_perf_ranks_dict
    ranked_perf_ranks_dict[
        f"{f_name}"
    ] = symbols_ranked_perf_ranks  # values: list of most common symbols in all performance ranks in descending order
    # pickle_dump(ranked_perf_ranks_dict, path_data_dump, f_pickled_ranked_perf_ranks_dict)
    # print(f'ranked_perf_ranks_dict:\n{ranked_perf_ranks_dict}\n')

    return perf_ranks_dict, ranked_perf_ranks_dict
