def plot_symbols(symbols, path_data_dump, date_start_limit=None,
                 date_end_limit=None, iloc_offset=None):
    """Plots symbol in symbols list. Program ps1n2 created dictionary
    dfs_symbols_OHLCV_download which has symbols' OHLCV data.
    The dictionary is stored in directory path_data_dump. This program plots
    the symbols using data from the dictionary.

    (Copied from def dates_within_limits)
    Order of hierarchy to determine Start and End dates:
    1. given date if it is not None
    2. iloc_offset if it is not None

    start = date_start_limit
    end = date_end_limit
    date_start_limit sets the upper (i.e. oldest) limit.
    date_end_limit sets the lower (i.e. newest) limit.
    date_start is the oldest index date that is within the limits.
    date_end is the newest index date that is within the limits.

    START   END    ILOC-OFFSET  Return->  START DATE             END DATE
    ---------------------------------------------------------------------------
    start   end	   iloc_offset	          date_start	         date_end
    start   end	   none                   date_start	         date_end
    start   none   iloc_offset	          date_start	         date_start+iloc_offset  # NOQA
    start   none   none                   date_start	         index[-1]
    none	end	   iloc_offset	          date_end-iloc_offset   date_end
    none	end	   none                   index[0]	             date_end
    none	none   iloc_offset	          index[0]	             index[-1]
    none	none   none                   index[0]	             index[-1]

    Args:
        symbols(list[str]): list of symbols, e.g. ['AAPL', 'GOOGL', ...]
        path_symbol_data(str): directory path of the symbol data
        date_start_limit(str): limit on the start date in format 'yyyy-mm-dd'
        date_end_limit(str): limit on the end date in format 'yyyy-mm-dd'
        iloc_offset(int): index offset
    
    Return:
        cache_returned_by_plot:
            symbol(str): stock symbol, e.g. 'AMZN'
            date(str): date, e.g. '2018-01-05'
            UI_MW_short[-1](float): last value of UI_MW_short,
                Ulcer-Index / Moving-Window-Short
            UI_MW_long[-1](float): last value of UI_MW_long
                Ulcer-Index / Moving-Window-Long
            diff_UI_MW_short[-1](float): last value of diff_UI_MW_short
                difference of last two 'Ulcer-Index / Moving-Window-Short'
            diff_UI_MW_long[-1](float): last value of diff_UI_MW_long
                difference of last two 'Ulcer-Index / Moving-Window-Long'
    """

    from myUtils import pickle_load, dates_within_limits
    from CStick_DD_OBV_UIMW_Diff_UIMW_cache import candlestick

    print('+'*15 + '  ps4_plot_symbols(symbols, path_data_dump)  ' + '+'*15
          + '\n')

    # directories and file names
    # dfs_filename = 'dfs_symbols_OHLCV_download'
    dfs_filename = 'dfs_OHLCV'
    index_symbol = 'XOM'
    # list of cache. Stores cache returned by candlestick plot
    caches_returned_by_plot = []
    # read dfs
    dfs = pickle_load(path_data_dump, dfs_filename)
    date_index_all_dates = dfs[index_symbol].index
    # get iloc of date_end_limit in XOM's date index
    date_start, date_end, iloc_date_start, iloc_date_end = \
        dates_within_limits(date_index_all_dates, date_start_limit,
                            date_end_limit, iloc_offset)

    for symbol in symbols:
        df = dfs[symbol]
        df = df[date_start:date_end]
        print('plot symbol {} from {} to {}\n'
              .format(symbol, date_start, date_end))
        # cache_returned_by_plot = candlestick(symbol, df, plot_chart=False)
        cache_returned_by_plot = candlestick(symbol, df, plot_chart=True)
        caches_returned_by_plot.append(cache_returned_by_plot)

    print('{}\n'.format('-'*78))

    return caches_returned_by_plot

symbols = ['FTEC', 'BCI', 'BTC-USD', 'ETH-USD']
# last date of data
date_end_limit = '2022-08-09'
# date_end_limit = dt.date.today().strftime("%Y-%m-%d")
iloc_offset = 252  # number of days to plot

plot_symbols(
    symbols=symbols,
    path_data_dump=path_data_dump,
    date_start_limit=None,
    date_end_limit=date_end_limit,
    iloc_offset=iloc_offset,
)