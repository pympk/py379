def _2_split_train_val_test(
    df, s_train=0.7, s_val=0.2, s_test=0.1, verbose=False
):
    """Split df into training (df_train), validation (df_val)
    and test (df_test) and returns the splitted dfs

    Args:
        df(dataframe): dataframe to be splitted
        s_train(float): ratio of df_train / df
        s_val(float): ratio of df_val / df
        s_test(float): ratio of df_test / df

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


def _3_random_slices(len_df, n_samples, days_lookback, days_eval, verbose=False):
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
