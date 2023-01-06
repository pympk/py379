print('z_grp_top_set_syms:')
z_grp_top_set_syms = zip(max_lookback_slices, grp_top_set_syms_n_freq)
for i, (_lookback_slice, _top_set_syms_n_freq) in enumerate(z_grp_top_set_syms):
  print(f'{i + 1 } of {n_samples} max_lookback_slice')
  print(f'max_lookback_slice: {_lookback_slice}')
  print(f'top_set_syms_n_freq: {top_set_syms_n_freq}')
  print(f'start_eval: {_lookback_slice[1]}')
  print(f'end_eval:   {_lookback_slice[2]}')
  l_syms = []  # list to accumlate top set symbbols
  for sym_n_freq in _top_set_syms_n_freq:
    l_syms.append(sym_n_freq[0])
    print(f'symbol: {sym_n_freq[0]:>4},  freq: {sym_n_freq[1]:>2}')
  print(f'top symbols from max_lookback_slice: {l_syms}')  
  print('')  
