# stock/equity dict keys 
eqKeys = ['symbol', 'quoteType', 'longName', 'industry', 'sector', 'marketCap', 'revenueGrowth',
    'earningsGrowth', 'previousClose', 'revenuePerShare', 'forwardEps', 'trailingEps']
# ETF dict keys
etfKeys = ['symbol', 'quoteType',  'longName', 'category', 'totalAssets', 'beta3Year', 'navPrice', 'previousClose',
           'holdings',  'sectorWeightings']
# cryto dict keys
crytoKeys = ['symbol', 'quoteType', 'name',  'regularMarketPrice', 'volume', 'marketCap', 'circulatingSupply', 'startDate']

for symbol in symbols:
  print('='*60)  
  obj = yf.Ticker(symbol)    
  if obj.info['quoteType'] == 'EQUITY':  # its a stock
      for key in eqKeys:
            value = obj.info[key]
            if key == 'marketCap':
                print(f'{key:20}{value/1e9:>10,.3f}B')  # reformat to billions  
            else:
                if type(value) == str:  # its a string
                    print(f'{key:20}{value}')
                else:  # format as a number    
                    print(f'{key:20}{value:>10.3f}')
      print('')
  elif obj.info['quoteType'] == 'ETF':  # its an ETF
      for key in etfKeys:
        value = obj.info[key]
        if key == 'holdings':  # print ETF stock holdings 
            keyItems = (len(value))
            hd_heading = f"\n{'symbol':10}{'holding-percent':20}{'name'}"
            print(hd_heading)
            for i in range(keyItems):
                hd_symbol = value[i]['symbol']
                hd_pct = value[i]['holdingPercent']
                hd_name = value[i]['holdingName']
                hd_info = f'{hd_symbol:<10}{hd_pct:<20.3f}{hd_name}'
                print(hd_info)
        elif key == 'sectorWeightings':# print ETF sector weightings
            keyItems = (len(value))
            hd_heading = f"\n{'sector':30}{'holding-percent':20}"
            print(hd_heading)
            sectors_list = value
            for sector_dict in sectors_list:
                for k, v in sector_dict.items():
                    print (f'{k:30}{v:<20.3f}')
        elif key == 'totalAssets':
            print(f'{key:20}{value/1e9:<.3f}B')  # reformat to billions             
        else:    
          print(f'{key:20}{value}')
      print('')
  elif obj.info['quoteType'] == 'CRYPTOCURRENCY':
      for key in crytoKeys:
        value = obj.info[key]
        if key == 'marketCap' or key == 'volume':
            print(f'{key:20}{value/1e9:<,.3f}B')  # asset in billions
        elif key == 'circulatingSupply':
            print(f'{key:20}{value/1e6:<,.3f}M')  # asset in billions
        elif key == 'startDate':
            UTC_timestamp_sec = obj.info['startDate']  # Unix time stamp (i.e. seconds since 1970-01-01)
            # convert Unix UTC_timestamp_sec in sec. to yyyy-mm-dd,  'startDate': 1367107200
            startDate = datetime.fromtimestamp(UTC_timestamp_sec).strftime("%Y-%m-%d")
            print(f'{key:20}{startDate}')  # asset in billions    
        else:
            if type(value) == str:
                print(f'{key:20}{value}')
            else:    
                print(f'{key:20}{value:<10,.0f}')
      print('')
  else:
      print(f'{symbol} is {obj.info["quoteType"]}')
      print('')