def random_slices (df, n_samples, days_lookback, days_eval):
  """Pad target_arr with leading numpy.nan to length arr_len.

  Args:
      df(dataframe): dataframe
      n_samples(int): number of slices to return
      days_lookback(int):  number of days to lookback for training
      days_eval(int): number of days to forward for evaluation 

  Return:
      r_slices(list of tuples): target_arr padded to length arr_len
  """
  
  
  import random
  from random import randint

  # random.seed(0)  
  n_sample = 0
  days_total = days_lookback + days_eval
  print(f'days_lookback: {days_lookback}, days_eval: {days_eval}, days_total: {days_total}, len(df): {len(df)}')

  if days_total > len(df):
    msg_err = f'days_total: {days_total} must be less or equal to len(df): {len(df)}'
    raise SystemExit(msg_err)

  # random slices of iloc for train and eval that fits the days_lookback, days_eval and total len(df) constraints
  r_slices = []
  while n_sample < n_samples:
    n_rand = randint(0, len(df))    
    start_train = n_rand - days_lookback
    end_train = n_rand
    start_eval = n_rand
    end_eval = n_rand + days_eval
    if 0 <= start_train and end_eval <= len(df):
      r_slices.append((start_train, end_train, end_eval))
      n_sample += 1

  return r_slices    