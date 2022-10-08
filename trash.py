df_merged = df.merge(dfw, how='left', on='Date')
df_merged = df_merged.sort_values(by=['Date', 'Time'])
df_merged.reset_index(drop=True, inplace=True)  # drop current index
pickle_dump(df_merged, path_pickle_dump, 'df_grSale_weather')
df_merged = pickle_load(path_pickle_dump, 'df_grSale_weather')
df_merged