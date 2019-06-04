import numpy as np
import pandas as pd

try:
    arr = np.load('data_sent.npy')
    labels = [
      'id', 'text_work', 'fullname', 'html', 'likes',
      'replies', 'retweets', 'text_raw', 'timestamp', 
      'url', 'user', 'sen'
      ]
    df = pd.DataFrame(arr, columns=labels)
except FileNotFoundError:
    # Loading data
    labels = [
      'fullname', 'html', 'id', 'likes', 'replies', 'retweets',
      'text', 'timestamp', 'url', 'user'
      ]
    arr = np.load('data.npy')
    df_full = pd.DataFrame(arr, columns=labels)

    labels = ['id', 'text']
    arr = np.load('data_work.npy')
    df_stem = pd.DataFrame(arr, columns=labels)

    df = pd.merge(df_stem, df_full, how='left', on='id', suffixes=('_work', '_raw'))
    df['sen'] = np.nan

output = []

pd.options.mode.chained_assignment = None

for i in range(len(df)):
    try:
        if pd.isnull(df['sen'].iloc[i]):
            print(f'Tweet n°{i+1}')
            print(df['text_raw'].iloc[i])
            print('\n')
            print(df['text_work'].iloc[i])
            print('Which sentiment: (pos/neu/neg)')
            sen = input()
            df['sen'].iloc[i] = sen
            print('\n------------------------\n')
        else:
            pass
    except KeyboardInterrupt:
      print('Progression saved. Writing file ...')
      np.save('data_sent.npy', df.values)
      break