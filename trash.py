df_1_5 =df_dow_g.loc[1:5]
# df_1_5
df_1_5.columns = df_1_5.columns.droplevel(1)  # drop sum in column index
df_1_5.index = df_1_5.index.droplevel(0)  # drop DOW in row index
df_1_5 = df_1_5.groupby(['Item']).agg({'Date':['sum'], 'Qty':['sum'], 'Gross Sales':['sum']})
df_1_5.columns = df_1_5.columns.droplevel(1)  # drop sum in column index
df_1_5['Avg_Sales_per_day'] = df_1_5['Gross Sales'] / df_1_5['Date'] 
df_1_5['Avg_Qty_per_day'] = df_1_5['Qty'] / df_1_5['Date'] 
df_1_5 = df_1_5.sort_values(by=['Gross Sales'], ascending=False)
df_1_5 = df_1_5.head(15)
df_1_5