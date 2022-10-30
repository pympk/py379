df_dow = df[['DOW', 'Item', 'Date', 'Qty', 'Gross Sales']]
df_dow
df_dow_g = df_dow.groupby(['DOW', 'Item']).agg({'Date':['nunique'], 'Qty':['sum'], 'Gross Sales':['sum']})
df_15 =df_dow_g.loc[0:5]
# df_15
df_15.columns = df_15.columns.droplevel(1)  # drop sum in column index
# df_15.index = df_15.index.droplevel(0)  # drop DOW in row index
df_15 = df_15.groupby(['Item']).agg({'Date':['sum'], 'Qty':['sum'], 'Gross Sales':['sum']})
df_15.columns = df_15.columns.droplevel(1)  # drop sum in column index
df_15['Avg_Sales_per_day'] = df_15['Gross Sales'] / df_15['Date'] 
df_15['Avg_Qty_per_day'] = df_15['Qty'] / df_15['Date'] 
df_15 = df_15.sort_values(by=['Gross Sales'], ascending=False)
df_15 = df_15.head(15)
df_15

_xlabel = ''
_ylabel = f'Sunday Avg. Qty.'
_title = f'Sunday Average Item Quantity.' + date_str

# data
x = df_15.index
y = df_15['Avg_Qty_per_day']

# plot
fig, ax = plt.subplots()
ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
plt.xlabel(_xlabel)
plt.ylabel(_ylabel)
plt.title(_title, fontsize = _fontsize*_titlescale)
plt.xticks(rotation = 85)
plt.rcParams["figure.figsize"] = (12, 4)
plt.grid(True)
plt.show()