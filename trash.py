def yf_print_symbol_data(symbols):
    """Prints symbol data from yfinance yf.Ticker(symbol).info,
    and OHLCV data for the last 5 day.

    Args:
        symbols([str]): list of symbols, e.g. ['AAPL', 'GOOGL', ...]

    Return:
        symbols_stock(list): list of stock symbols
        symbols_etf(list): list of etf symbols
        symbols_cryto(list): list of cryto symbols
    """

    import yfinance as yf
    import textwrap
    import pandas as pd
    from datetime import datetime

    pd.set_option("display.width", 300)
    pd.set_option("display.max_columns", 10)

    # Wrapper for longBusinessSummary
    wrapper = textwrap.TextWrapper(width=60)

    # stock/equity dict keys for obj.info
    eqKeys = [
        "symbol",
        "quoteType",
        "longName",
        "industry",
        "sector",
        "marketCap",
        "revenueGrowth",
        "earningsGrowth",
        "earningsQuarterlyGrowth",
        "ebitdaMargins",
        "previousClose",
        "fiftyTwoWeekHigh",
        "52WeekChange",
        "revenuePerShare",
        "forwardEps",
        "trailingEps",
        "sharesOutstanding",
        "longBusinessSummary",
    ]
    # ETF dict keys for obj.info
    etfKeys = [
        "symbol",
        "quoteType",
        "longName",
        "category",
        "totalAssets",
        "beta3Year",
        "navPrice",
        "previousClose",
        "holdings",
        "sectorWeightings",
        "longBusinessSummary",
    ]
    # cryto dict keys for obj.info
    crytoKeys = [
        "symbol",
        "quoteType",
        "name",
        "regularMarketPrice",
        "volume",
        "marketCap",
        "circulatingSupply",
        "startDate",
    ]

    symbols_stock = []  # symbols that are stocks
    symbols_etf = []  # symbols that are ETFs
    symbols_cryto = []  # symbols that are crytos

    for symbol in symbols:
        print("=" * 60)
        # print symbol OHLCV for the last 5 days
        print(f'{symbol}\n{yf.Ticker(symbol).history(period="5d")}\n')
        obj = yf.Ticker(symbol)  # dir(obj) lists methods in obj
        # obj.info is a dict (e.g {'exchange': 'PCX', ... ,  'logo_url': ''})
        if obj.info["quoteType"] == "EQUITY":  # its a stock
            symbols_stock.append(symbol)
            for key in eqKeys:
                value = obj.info[key]
                if key == "marketCap":
                    print(
                        f"{key:26}{value/1e9:>10,.3f}B"
                    )  # reformat to billions
                elif key == "sharesOutstanding":
                    print(
                        f"{key:26}{value/1e6:>10,.3f}M"
                    )  # reformat to millions

                elif key == "longBusinessSummary":
                    string = wrapper.fill(text=value)
                    print(f"\n{key}:\n{string}")                    
                else:
                    # if type(value) == str:  # its a string
                    if type(value) == str or value == None:  # its a string 
                        print(f"{key:26}{value}")
                    else:  # format as a number
                        print(f"{key:26}{value:>10.3f}")
            print("")
        elif obj.info["quoteType"] == "ETF":  # its an ETF
            symbols_etf.append(symbol)
            for key in etfKeys:
                value = obj.info[key]
                # obj.info['holding'] is a list of of dict
                #   e.g. [{'symbol': 'AAPL', 'holdingName': 'Apple Inc', 'holdingPercent': 0.2006}, ...]
                if key == "holdings":  # print ETF stock holdings
                    keyItems = len(value)
                    hd_heading = (
                        f"\n{'symbol':10}{'holding-percent':20}{'name'}"
                    )
                    print(hd_heading)
                    for i in range(keyItems):
                        hd_symbol = value[i]["symbol"]
                        hd_pct = value[i]["holdingPercent"]
                        hd_name = value[i]["holdingName"]
                        hd_info = f"{hd_symbol:<10}{hd_pct:<20.3f}{hd_name}"
                        print(hd_info)
                # obj.info['sectorWeightings'] is a list of of dict, similar to obj.info['holding']
                elif key == "sectorWeightings":  # print ETF sector weightings
                    keyItems = len(value)
                    hd_heading = f"\n{'sector':30}{'holding-percent':20}"
                    print(hd_heading)
                    sectors_list = value
                    for sector_dict in sectors_list:
                        for k, v in sector_dict.items():
                            print(f"{k:30}{v:<20.3f}")
                elif key == "totalAssets":
                    print(f"{key:26}{value/1e9:<.3f}B")  # reformat to billions
                elif key == "longBusinessSummary":
                    string = wrapper.fill(text=value)
                    print(f"\n{key}:\n{string}")    
                else:
                    print(f"{key:26}{value}")
            print("")
        elif obj.info["quoteType"] == "CRYPTOCURRENCY":
            symbols_cryto.append(symbol)
            for key in crytoKeys:
                value = obj.info[key]
                if key == "marketCap" or key == "volume":
                    print(
                        f"{key:26}{value/1e9:>10,.3f}B"
                    )  # reformat to billions
                elif key == "circulatingSupply":
                    print(
                        f"{key:26}{value/1e6:>10,.3f}M"
                    )  # reformat to millions
                elif key == "startDate":
                    UTC_timestamp_sec = obj.info[
                        "startDate"
                    ]  # Unix time stamp (i.e. seconds since 1970-01-01)
                    # convert Unix UTC_timestamp_sec in sec. to yyyy-mm-dd,  'startDate': 1367107200
                    startDate = datetime.fromtimestamp(
                        UTC_timestamp_sec
                    ).strftime("%Y-%m-%d")
                    print(f"{key:26}{startDate}")  # reformat to billions
                else:
                    if type(value) == str:
                        print(f"{key:26}{value}")
                    else:
                        print(f"{key:26}{value:>10,.0f}")
            print("")
        else:
            print(f'{symbol} is {obj.info["quoteType"]}')
            print("")

    return symbols_stock, symbols_etf, symbols_cryto
