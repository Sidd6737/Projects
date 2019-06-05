# -*- coding: utf-8 -*-
"""
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:34:32 2019

@author: siddharth Desai
"""

#import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from IPython import get_ipython
from matplotlib.pylab import rcParams
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from fastai.tabular import  add_datepart
from sklearn.linear_model import LinearRegression
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

get_ipython().run_line_magic('matplotlib', 'inline')
register_matplotlib_converters()
#setting figure size
rcParams['figure.figsize'] = 20,10

#for normalizing data
scaler = MinMaxScaler(feature_range=(0, 5))

#read the file
stocks = pd.read_csv('aapl.csv')

#print stocks
print ("This gives us all the data that will be used in the analysis\n",stocks.head(21))

#print analysis
print ("This is the Analyis of the All data in the File\n :",stocks.describe())

#print Dimensions
print ("Number Of Dimensions: ",stocks.ndim)

#print Dataframe
print ("DataFrame of the Sample :",stocks.shape)

#setting index as date
stocks['Date'] = pd.to_datetime(stocks.Date,format='%d-%m-%Y')
stocks.index = stocks['Date']

#plot
plt.figure(figsize=(2,1))
plt.plot(stocks['Close'], label='Close Price history')

###############################################################################
                                


###############################################################################
                            #Linear_Agression

#setting index as date values
stocks['Date'] = pd.to_datetime(stocks.Date,format='%Y-%m-%d')
stocks.index = stocks['Date']

#sorting
data = stocks.sort_index(ascending=True, axis=0)

#creating a separate dataset
new_data = pd.DataFrame(index=range(0,len(stocks)),columns=['Date', 'Close'])

for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]
    
#create features
add_datepart(new_data, 'Date')
new_data.drop('Elapsed', axis=1, inplace=True)  #elapsed will be the time stamp
new_data['mon_fri'] = 0

for i in range(0,len(new_data)):
    if (new_data['Dayofweek'][i] == 0 or new_data['Dayofweek'][i] == 4):
        new_data['mon_fri'][i] = 1
    else:
        new_data['mon_fri'][i] = 0

#split into train and validation
train = new_data[:542]
valid = new_data[542:]
x_train = train.drop('Close', axis=1)
y_train = train['Close']
x_valid = valid.drop('Close', axis=1)
y_valid = valid['Close']

#implement linear regression
model = LinearRegression()
model.fit(x_train,y_train)

#make predictions and find the rmse
preds = model.predict(x_valid)
rms=np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds)),2)))
print (rms)

#plot
valid['Predictions'] = 0
valid['Predictions'] = preds

valid.index = new_data[542:].index
train.index = new_data[:542].index

plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])

###############################################################################
                                    #K_Nearest_Neighbours

#scaling data
scaler = MinMaxScaler(feature_range=(0, 1))
x_train_scaled = scaler.fit_transform(x_train)
x_train = pd.DataFrame(x_train_scaled)
x_valid_scaled = scaler.fit_transform(x_valid)
x_valid = pd.DataFrame(x_valid_scaled)

#using gridsearch to find the best parameter
params = {'n_neighbors':[2,3,4,5,6,7,8,9]}
knn = neighbors.KNeighborsRegressor()
model = GridSearchCV(knn, params, cv=5)

#fit the model and make predictions
model.fit(x_train,y_train)
preds = model.predict(x_valid)

#rmse
rms=np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds)),2)))
print (rms)

#plot
valid['Predictions'] = 0
valid['Predictions'] = preds
plt.plot(valid[['Close', 'Predictions']])
plt.plot(train['Close'])

#####################################################################################################################
                                    #Long_Short_Term_Memory

#creating dataframe
data = stocks.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0,len(stocks)),columns=['Date', 'Close'])
for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]

#setting index
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)

#creating train and test sets
dataset = new_data.values
train = dataset[0:542,:]
valid = dataset[542:,:]

#converting dataset into x_train and y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
x_train, y_train = [], []

for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

#predicting 540 values, using past 50 from the train data
inputs = new_data[len(new_data) - len(valid) - 50:].values
inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)
X_test = []

for i in range(50,inputs.shape[0]):
    X_test.append(inputs[i-50:i,0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)

#Implementation
rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
print (rms)

#for plotting
train = new_data[:542]
valid = new_data[542:]
valid['Predictions'] = closing_price
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])

###############################################################################