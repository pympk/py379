import numpy as np
UIMW15 = np.apply_along_axis(UIMW15, 0, drawdown)
UIMW30 = np.apply_along_axis(UIMW30, 0, drawdown)
print(f'UIMW15.shape : {UIMW15.shape}')
print(f'UIMW30.shape : {UIMW30.shape}')