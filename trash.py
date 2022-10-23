# print df of each unique values in level 0
# 0 = 0
_idx_names = _df.index.names
_dict = {'DOW': 'Days-of-week', 0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat'}
_dict[_idx_names[0]]
items_in0 = _df.index.unique(level=0)
# print(f'items_in0_{0}: {items_in0}')
# print(f'items in level: {0} (index name: {_idx_names[0]}): {items_in0}')  
print(f'items in level: {0}, index name: {_idx_names[0]} ({_dict[_idx_names[0]]}): {items_in0}\n')  
for unique_item in items_in0:
  print(f'level {0}, unique item: {unique_item} ({_dict[unique_item]})')
  # print(_df.loc[unique_item].index.names[0])    
  print(_df.loc[unique_item].index.names[0])  
  print(_df.loc[unique_item].index.unique(level=0))
  print('')