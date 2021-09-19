import yahoo_fin.stock_info as si
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import math
import tensorflow as tf 
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go



def predict(ticker):
    df = si.get_data(ticker, start_date="01/01/2000", end_date="12/31/2020", interval="1d")
    df.reset_index(level=0, inplace=True)
    df.columns = ['Date', 'Open', 'High','Low','Close','Adclose','Volume','Ticker']
    
    #Get index len
    ilen = len(df.index)/2
    ilen = math.floor(ilen)


    # First calculate the mid prices from the highest and lowest
    high = df.loc[:,'High'].to_numpy()
    low = df.loc[:,'Low'].to_numpy()
    mid = (high+low)/2.0
    #set up to train data
    train = mid[:ilen]
    test = mid[ilen:]
    
    scaler = MinMaxScaler()
    train = train.reshape(-1,1)
    test = test.reshape(-1,1)

    # Train the Scaler with training data and smooth data
    smoothing_window_size = 2500
    for di in range(0,1000,smoothing_window_size):
        scaler.fit(train[di:di+smoothing_window_size,:])
        train[di:di+smoothing_window_size,:] = scaler.transform(train[di:di+smoothing_window_size,:])
    
    # exponential moving average smoothing
    #gives a smoother curve 
    EMA = 0.0
    G = 0.1
    for ti in range(ilen):
      EMA = G*train[ti] + (1-G)*EMA
      train[ti] = EMA

    #Prediction algo, uses standard average which is best to see for the following day
    all_mid_data = np.concatenate([train,test],axis=0)
    window_size = 30
    N = train.size
    avg_predictions = []
    avg_x = []
    mse_errors = []

    for pred_idx in range(window_size,N):

        if pred_idx >= N:
            date = dt.datetime.strptime(k, '%Y-%m-%d').date() + dt.timedelta(days=1)
        else:
            date = df.loc[pred_idx,'Date']

        avg_predictions.append(np.mean(train[pred_idx-window_size:pred_idx]))
        mse_errors.append((avg_predictions[-1]-train[pred_idx])**2)
        avg_x.append(date)
    out_mid_data = np.concatenate(all_mid_data[:2297]).ravel().tolist()
    print('MSE error for standard averaging: %.5f'%(0.5*np.mean(mse_errors)))
    

    
    

    fig = go.Figure()
    fig = go.Figure(data=go.Scatter(x=list(range(window_size,N)), y= avg_predictions[:2297], name="Prediction"))
    fig.add_trace(go.Scatter(x=list(range(2297)), y=out_mid_data, mode='lines',name='True'))
    fig.update_layout(
    xaxis_title="Days",
    yaxis_title="Average Price",)
    fig.show()
    
    
 
 
 




