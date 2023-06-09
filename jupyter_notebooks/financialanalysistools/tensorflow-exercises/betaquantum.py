
#Source and credit: https://github.com/MSKX/tensorflow-quantum_dense
#Confirm successful import of packages
import numpy as np
import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as plt_dates

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from QuantumDense import VQNNModel

import matplotlib.dates as plt_dates

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from QuantumDense import VQNNModel

#Confirm successful import of input data, instead of refinitive.dataplatform.eikon API
import yfinance as yf
import pandas as pd
import datetime as date


now = date.date.today()
today = now.strftime('%Y-%m-%d')
yesterday = (now - pd.Timedelta('1day')).strftime('%Y-%m-%d')
ninedaysago = (now - pd.Timedelta('9day')).strftime('%Y-%m-%d')

# read input data from CSV file
df = pd.read_csv('datasets/test.csv')

# convert date column to datetime and set as index
df['DATE'] = pd.to_datetime(df['DATE'])
df.set_index('DATE', inplace=True)
df['HL_DELTA'] = df['HIGH'] - df['LOW']
df['RETURNS'] = df['CLOSE'].pct_change()
df['PRX_MA_ND'] = df['CLOSE'].rolling(window=5).mean()
df['VOLATILITY'] = df['CLOSE'].rolling(window=5).std()
df['TP1_RETURNS'] = df['RETURNS'].shift(-1)

df.dropna(inplace=True)


print(df)

#Create 3 dimensional Tensor
df_x = df[['RETURNS', 'VOLUME', 'PRX_MA_ND', 'VOLATILITY']]
df_y = df['TP1_RETURNS']
df_x.dropna(inplace=True)
df_x

df_y #check

df_x_scaler = MinMaxScaler().fit(df_x)

forward_test_date = '2022-10-01'

fdf_x = df_x.loc[forward_test_date:]
fdf_y = df_y.loc[forward_test_date:]
df_x = df_x.loc[:forward_test_date]
df_y = df_y.loc[:forward_test_date]

fdf_prx = df.loc[forward_test_date:]['CLOSE']
fdf_y_len = len(fdf_y)

df_x_scaled = pd.DataFrame(df_x_scaler.transform(df_x))
fdf_x_scaled = pd.DataFrame(df_x_scaler.transform(fdf_x))

x_train, x_test, y_train, y_test = train_test_split(df_x_scaled,
                                                    df_y,
                                                    test_size=0.25,
                                                    random_state=42)

x_train

x_train = np.expand_dims(x_train.values, 1).astype(np.float32)
y_train = np.expand_dims(y_train.values, 1).astype(np.float32)
x_validation = np.expand_dims(x_test.values, 1).astype(np.float32)
y_validation = np.expand_dims(y_test.values, 1).astype(np.float32)

qnn_model = VQNNModel()
qnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001,
                                                     beta_1=0.9,
                                                     beta_2=0.999,
                                                     epsilon=1e-07),
                  loss=tf.keras.losses.MeanSquaredError(),
                  metrics=["mean_squared_error"])
qnn_model.run_eagerly = True