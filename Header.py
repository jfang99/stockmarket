#Imports
import urllib
import json
import numpy as np
import sys
import math
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.optimizers import Adam
from keras.layers import BatchNormalization
from keras import regularizers
import matplotlib.pyplot as plt


#API request
ticker = sys.argv[1]

url = "https://www.blackrock.com/tools/hackathon/performance?identifiers="  + ticker 
parameters = {
'betaPortfolios' :  "SNP500",
'identifiers' :  ticker,
'includePrices' :  "true",
'riskFreeRatePortfolio' :  "LTBILL1-3M"
}
  
query_string = urllib.parse.urlencode(parameters)      
url = url + "?" + query_string

req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
respData = resp.read().decode('utf-8')
json_obj = json.loads(respData)


#Prase result data
resultMap = json_obj['resultMap']
returns = resultMap['RETURNS'][1]
returnsMap = returns['returnsMap']
performanceChart = returns['performanceChart']

date_list = []
level_list = []
for dates in returnsMap:
  date_list.append(dates)
  level_list.append(returnsMap[dates]['level'])
  

#Hyperprams
window_size = 64
sma_strength = 0.8
split_idx = math.floor(0.85 * len(level_list))

#Preprocessing
levels = np.array(level_list)
train = levels[0:split_idx]
test = levels[split_idx-window_size:]
#print(train.shape)
#print(test.shape)

scaler = StandardScaler()
#scaler = MinMaxScaler(feature_range=(0, 1))

train = scaler.fit_transform(train.reshape((-1,1)))
test = scaler.transform(test.reshape((-1,1)))


x_train, y_train = [], []
for i in range(window_size,len(train)):
    x_train.append(train[i-window_size:i])
    y_train.append(train[i])
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))


x_test = []
for i in range(window_size,test.shape[0]):
    x_test.append(test[i-window_size:i])
    
x_test = np.array(x_test)
sma = np.mean(x_test,axis = 1)
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

#print('================')
#print(x_train.shape)
#print(y_train.shape)
#print(x_test.shape)

#print(sma.shape)


#LSTM model
model = Sequential()
model.add(LSTM(units=64, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=32))

model.add(BatchNormalization(momentum=0.01, epsilon=1e-3))
model.add(Dropout(0.2))
model.add(Dense(1))

optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, decay=0.95)

model.compile(loss='mean_squared_error', optimizer=optimizer)
model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=0,validation_split = 0.1, shuffle=True)

#Make predictions
y_pred = model.predict(x_test)
y_pred = scaler.inverse_transform(y_pred)
#y_pred *= ( sma_strength * sma)
#print(y_pred.shape)


#Plot and send out data
y_pred_plot = np.vstack((levels[: -len(y_pred)].reshape(-1,1), y_pred))

plt.figure(figsize=(16,9))
plt.plot(level_list, label='Ground Truth Prices')
plt.plot(y_pred_plot, label='Predicted Prices')
plt.plot(levels[: -len(y_pred)], label='Price history')

plt.xlabel('Days since start date')
plt.ylabel('Change comparing with start date')
plt.legend()

plt.savefig('images.jpeg')
print(str(y_pred[-1]))

