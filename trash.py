# place 0.000001 in the last row where columns in the 2d drawdown array are all zeros
#   prevent UI calculation to be 0, and CAGR/UI to be infinite 
_cols = np.all(arr_drawdown==0, axis=0)  # True if column is all 0, i.e. the symbol does not have drawdown
_arr_drawdown_last_row = arr_drawdown[-1]  # get the last row

for _i, _cond in enumerate(_cols):
  if _cond:
    _arr_drawdown_last_row[_i] = 0.000001  # replace zero with a small value  

arr_drawdown[-1] = _arr_drawdown_last_row  # replace the last row
arr_drawdown     
