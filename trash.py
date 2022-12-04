def random_slices(len_df, n_samples, days_lookback, days_eval, verbose=False):
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
