def _5_lookback_slices(max_slices, days_lookbacks, verbose=False):
    """
    Create sets of sub-slices from max_slices and days_lookbacks. A slice is
    a tuple of iloc values for start_train:end_train=start_eval:end_eval.
    Given 2 max_slices of [(104, 224, 234), (626, 746, 756)], it returns 2 sets
    [[(194, 224, 234), (164, 224, 234), (104, 224, 234)],
    [(716, 746, 756), (686, 746, 756), (626, 746, 756)]]. End_train is constant
    for each set. End_train-start_train is the same value from max_slice.

    Args:
        max_slices(list of tuples): list of iloc values for
        start_train:end_train=start_eval:end_eval, where end_train-start_train
        is the max value in days_lookbacks
        days_lookback(int):  number of days to lookback for training

    Return:
        lb_slices(list of lists of tuples): each sublist is set of iloc for
        start_train:end_train:end_eval tuples, where the days_lookbacks are
        the values of end_train-start_train in the set, and end_train-end_eval
        are same values from max_slices. The number of sublist is equal to
        number of max_slices. The number of tuples in the sublists is equal to
        number
    """

    lb_slices = []
    days_lookbacks.sort()  # sort list of integers in ascending order
    for max_slice in max_slices:
        l_max_slice = []
        for days in days_lookbacks:
            new_slice = (max_slice[1] - days, max_slice[1], max_slice[2])
            l_max_slice.append(new_slice)
            if verbose:
                print(f"days: {days}, {new_slice}")
        lb_slices.append(l_max_slice)
        if verbose:
            print("")

    return lb_slices
