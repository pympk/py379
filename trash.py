def _6_grp_tuples_sort_sum(l_tuples, reverse=True):
    # https://stackoverflow.com/questions/2249036/grouping-python-tuple-list
    # https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
    """
    Given a list of tuples of (key:value) such as:
    [('grape', 100), ('apple', 15), ('grape', 3), ('apple', 10),
     ('apple', 4), ('banana', 3)]
    Returns list of grouped-sorted-tuples based on summed-values such as:
    [('grape', 103), ('apple', 29), ('banana', 3)]

    Args:
        l_tuples(list of tuples): list of tuples of key(str):value(int) pairs
        reverse(bool): sort order of summed-values of the grouped tuples,
         default is descending order.

    Return:
        grp_sorted_list(list of tuples): list of grouped-sorted-tuples
         based on summed-values such as:
         [('grape', 103), ('apple', 29), ('banana', 3)]
    """

    import itertools
    from operator import itemgetter

    grp_list = []
    sorted_tuples = sorted(l_tuples)
    it = itertools.groupby(sorted_tuples, itemgetter(0))

    for key, subiter in it:
        # print(f'key: {key}')
        key_sum = sum(item[1] for item in subiter)
        # print(f'key_sum: {key_sum}')
        grp_list.append((key, key_sum))

    grp_sorted_list = sorted(grp_list, key=itemgetter(1), reverse=reverse)

    return grp_sorted_list
