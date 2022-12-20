def symb_perf_stats_vectorized_v2(df_symbols_close):
    """Takes dataframe of symbols' close and returns symbols, period_yr,
       drawdown, UI, max_drawdown, returns_std, Std_UI, CAGR, CAGR_Std, CAGR_UI
       https://stackoverflow.com/questions/36750571/calculate-max-draw-down-with-a-vectorized-solution-in-python
       http://www.tangotools.com/ui/ui.htm
       Calculation CHECKED against: http://www.tangotools.com/ui/UlcerIndex.xls
       Calculation VERIFIED in: symb_perf_stats_vectorized.ipynb

    Args:
        df_symbols_close(dataframe): dataframe with date as index,
          symbol's close in columns, and symbols as column names.

    Return:
        symbols(pandas.core.indexes.base.Index): stock symbols
        period_yr(float): years, (days in dataframe) / 252
        drawdown(pandas dataframe): drawdown from peak, 0.05 means 5% drawdown,
            with date index and symbols as column names
        UI(pandas.series float64): ulcer-index
        max_drawdown(pandas series float64): maximum drawdown from peak
        returns_std(pandas series float64): standard deviation of daily returns
        Std_UI(pandas series float64): returns_std / UI
        CAGR(pandas series float64): compounded annual growth rate
        CAGR_Std(pandas series float64): CAGR / returns_std
        CAGR_UI(pandas series float64): CAGR / UI
    """
    # v1 convert drawdown from pandas series to numpy array
    # v2 do calculation in numpy array

    import numpy as np
    import pandas as pd

    dates = df_symbols_close.index
    symbols = df_symbols_close.columns
    len_df = len(df_symbols_close)

    arr = df_symbols_close.to_numpy()
    arr_returns = arr / np.roll(arr, 1, axis=0) - 1
    arr_returns_std = np.std(arr_returns[1:, :], axis=0, ddof=1)  # drop first row 
    arr_returns[0] = 0  # set first row to 0 
    arr_cum_returns = (1 + arr_returns).cumprod(axis=0)  # cumulative product of column elements
    # accumulative max value of column elements 
    arr_drawdown = arr_cum_returns / np.maximum.accumulate(arr_cum_returns, axis=0) -1
    arr_max_drawdown = arr_drawdown.min(axis=0)    
    arr_UI = np.sqrt(np.sum(np.square(arr_drawdown), axis=0) / len_df)
    arr_Std_UI = arr_returns_std / arr_UI
    Std_UI = pd.Series(arr_Std_UI, index=symbols)
    period_yr = len_df / 252  # 252 trading days per year
    arr_CAGR = (arr[-1] / arr[0]) ** (1 / period_yr) - 1
    arr_CAGR_Std = arr_CAGR / arr_returns_std
    arr_CAGR_UI = arr_CAGR / arr_UI

    # convert numpy array to dataframe, add date index and symbols as column names
    drawdown = pd.DataFrame(arr_drawdown, index=dates, columns=symbols)
    # convert numpy array to pandas series, add symbols as index    
    UI = pd.Series(arr_UI, index=symbols)
    max_drawdown = pd.Series(arr_max_drawdown, index=symbols)
    returns_std = pd.Series(arr_returns_std, index=symbols)
    CAGR = pd.Series(arr_CAGR, index=symbols)
    CAGR_Std = pd.Series(arr_CAGR_Std, index=symbols)
    CAGR_UI = pd.Series(arr_CAGR_UI, index=symbols)

    return symbols, period_yr, drawdown, UI, max_drawdown, \
        returns_std, Std_UI, CAGR, CAGR_Std, CAGR_UI
