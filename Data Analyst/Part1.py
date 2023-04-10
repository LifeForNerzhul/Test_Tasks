import pandas as pd
import numpy as np
import random
import decimal


colors = ('red', 'white', 'blue', 'black', 'pink', 'green', 'brown', 'orange', 'yellow')

pd.set_option('max_rows', 300)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.3f}'.format)

df = pd.read_excel('Тестовое задание.xlsx',)
print('Previous Datatypes\n', df.dtypes, sep='')

# Delete hidden column
df = df.drop(columns='good (1)', axis=1)
# Validate data type
for i in range(len(df)):
    if type(df.loc[i, 'cluster']) is not np.float64:
        df.loc[i, 'cluster'] = pd.NaT
    if type(df.loc[i, 'count']) is not float:
        df.loc[i, 'count'] = pd.NaT
    if type(df.loc[i, 'x']) is not np.float64:
        df.loc[i, 'x'] = pd.NaT
    try:
        df.loc[i, 'y'] = decimal.Decimal(df.loc[i, 'y'])
    except AttributeError:
        df.loc[i, 'y'] = pd.NaT
    except ValueError:
        df.loc[i, 'y'] = pd.NaT
    except decimal.InvalidOperation:
        df.loc[i, 'y'] = pd.NaT

df = df.dropna(axis=0).reset_index(drop=True)
df = df.astype({'cluster': int, 'count': int, 'x': float, 'y': float})      # 'y' was 'object' type

# delete duplicates
df = df.drop_duplicates(subset=['area', 'keyword'], keep='first', inplace=False).reset_index(drop=True)

# add color
df['color'] = 0
i = 1
df.loc[0, 'color'] = random.choice(colors)
used_colors = {df.loc[0, 'color']}
while i <= len(df.index) - 1:
    # add color while same cluster and area
    while df.loc[i, 'cluster'] == df.loc[i - 1, 'cluster'] and df.loc[i, 'area'] == df.loc[i - 1, 'area']:
        df.loc[i, 'color'] = df.loc[i - 1, 'color']
        i += 1
        if i == len(df.index):      # stop or index out of range
            break
    if i == len(df.index):          # stop or index out of range
        break
    # color for next cluster/area
    df.loc[i, 'color'] = random.choice(colors)
    # if new area we can use colors again
    if df.loc[i, 'area'] != df.loc[i - 1, 'area']:
        used_colors = {df.loc[i, 'color']}
    # change color while it in used_colors
    while df.loc[i, 'color'] in used_colors:
        df.loc[i, 'color'] = random.choice(colors)
    # add color in set so we can compare
    used_colors.add(df.loc[i, 'color'])
    i += 1

df = df.sort_values(['area', 'cluster', 'cluster_name', 'count'], ascending=(True, True, True, False))    # False - по возрастанию
df = df.dropna(axis=0).reset_index(drop=True)

df.to_excel('result.xlsx', index=False, freeze_panes=(1, 0))
