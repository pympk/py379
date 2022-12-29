# grp_perf_ranks = {}
grp_most_common_syms = []
# loop thru lists of tuples of start_train:end_train:end_eval, i.e.
#  [[(887, 917, 927), (857, 917, 927), (797, 917, 927)],
#  [(483, 513, 523), (453, 513, 523), (393, 513, 523)]]
for lb_slices in all_lb_slices:  
  for lb_slice in lb_slices:  # lb_slice, e.g. (246, 276, 286)
    start_train = lb_slice[0]
    end_train = lb_slice[1]
    start_eval = end_train
    end_eval = lb_slice[2]
    lookback = end_train - start_train
    eval = end_eval - start_eval
    print(f'lb_slices:     {lb_slices}')
    print(f'lb_slice:      {lb_slice}')
    print(f'days lookback: {lookback}')
    print(f'days eval:     {eval}')    
    print(f'start_train:   {start_train}')
    print(f'end_train:     {end_train}')
    # print(f'start_eval:    {start_eval}')
    # print(f'end_eval:      {end_eval}')

    _df = df_train.iloc[start_train:end_train]
    perf_ranks, most_common_syms = _4_perf_ranks(_df, n_top_syms=10)
    # 1 lookback of r_CAGR/UI, r_CAGR/retnStd, r_retnStd/UI
    print(f'perf_ranks: {perf_ranks}')  
    # most common symbols of perf_ranks 
    print(f'most_common_syms: {most_common_syms}')     
    # grp_perf_ranks[lookback] = perf_ranks
    print(f'+++ finish lookback {lookback} +++')
    grp_most_common_syms.append(most_common_syms)
    
  print(f'grp_most_common_syms: {grp_most_common_syms}')
  print(f'===== finish lookback slice {lb_slice} ====='\n)