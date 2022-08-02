def symbols_close(
    path_dir,
    path_data_dump,
    filename_pickled_df_OHLCV,
    verbose=False,
):
    """Reads adjusted OHLCV data for symbols in pickled df_OHLCV and gathers 
       symbols' Close into df_symbols_close. It has a date index and the
       column names are the symbols. Rows and columns with all NaN are dropped.

       Usage: df_symbols_close['SPY'] returns a series with date index and 
       SPY Close

    Args:
        path_dir(str): directory path of df_OHLCV
        path_data_dump(str): directory of pickled files
        filename_pickled_df_OHLCV(str): filename of df_OHLCV
        verbose(bool): prints output if True, default False

    Return:
        df_symbols_close(dataframe): dataframe with a date index and 
            columns of symbols' Close, column names are symbols 
        dates_dropped(DatetimeIndex): dates where all symbols' Close are NaN
        symbols_OHLCV(list): symbols in df_OHLCV
        symbols_dropped(list): symbols where their Close is all NaN 
    """

    import pandas as pd
    from myUtils import pickle_load, pickle_dump

    df = pickle_load(
        path_data_dump, filename_pickled_df_OHLCV, verbose=verbose
    )
    # get list of symbols in df_OHLCV, list(df) is a list of tuples
    # e.g.: [('AAPL', 'Open')..('AAPL', 'Volume'),...
    #        ('ZZZZ', 'Open')..('ZZZZ', 'Volume')]
    symbols_OHLCV = list(set([i[0] for i in list(df)]))

    # write symbols' Close to df_symbols_close
    for sym in symbols_OHLCV:
        if (
            sym == symbols_OHLCV[0]
        ):  # create dataframe using the 1st symbol's Close
            df_symbols_close = pd.DataFrame(df[symbols_OHLCV[0]].Close)
        else:  # concatenate Close on subsequent symbols
            df_symbols_close = pd.concat(
                [df_symbols_close, df[sym].Close], axis=1
            )
    # rename column names from Close to symbol names
    df_symbols_close.set_axis(symbols_OHLCV, axis=1, inplace=True)

    # drop rows and columns with all NaN
    print(f"df_symbols_close.info before dropna:\n{df_symbols_close.info()}")
    df_symbols_close_index_before_dropna = df_symbols_close.index
    df_symbols_close = df_symbols_close.dropna(
        how="all", axis="index"
    )  # drop all NaN rows
    df_symbols_close = df_symbols_close.dropna(
        how="all", axis="columns"
    )  # drop all NaN columns
    print(f"df_symbols_close.info after dropna:\n{df_symbols_close.info()}")
    # dates with all NaN in row
    dates_dropped = df_symbols_close_index_before_dropna.difference(
        df_symbols_close.index
    )
    # symbols (i.e. column names) with all NaN in column
    symbols_dropped = list(set(symbols_OHLCV) - set(list(df_symbols_close)))

    pickle_dump(
        df_symbols_close, path_data_dump, "df_symbols_close", verbose=verbose
    )
    pickle_dump(
        dates_dropped,
        path_data_dump,
        "df_OHLCV_dates_dropped",
        verbose=verbose,
    )
    pickle_dump(
        symbols_dropped,
        path_data_dump,
        "df_OHLCV_symbols_dropped",
        verbose=verbose,
    )

    return df_symbols_close, dates_dropped, symbols_OHLCV, symbols_dropped
