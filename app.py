from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import holidays
import tensorflow as tf
from keras.models import load_model

model = load_model("fetch_model.h5")

app = Flask(__name__, static_url_path='/static')
scaler=joblib.load('receipt_scaler.joblib')


def prepareData(df):
    # I tried to find out the area fetch operates on , I feel its mainly north america.
    # hence US and canada holidays are considered.
    df['date'] = pd.to_datetime(df['date'])
    ca_holidays = holidays.CA(years=2021)
    us_holidays = holidays.US(years=2021)
    h_tag=[]
    dayofweek=[]
    day=[]
    month=[]
    weekofyear=[]
    ind=0
    for i in df['date']:
        dayofweek.append(i.dayofweek)
        day.append(i.day)
        month.append(i.month)
        weekofyear.append(i.weekofyear)
        if i in us_holidays:
            h_tag.append(1)
        elif i in ca_holidays:
            h_tag.append(1)
        else:
            h_tag.append(0)

        ind=ind+1
    df['holidays']=h_tag
    df['day']=day
    df['month']=month
    df['dayofweek']=dayofweek
    df['weekofyear']=weekofyear
    del df['date']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    startDate=datetime.strptime(data['startDate'], '%Y-%m-%d')
    # startDate=data['startDate']
    print(type(startDate))
    counts=data['counts']
    dates=[]
    rcount=[]
    for i in range(0,7):
        dates.append(startDate)
        startDate=startDate+timedelta(days=1)
        rcount.append(counts[i]['count'])
    dates.append(startDate)

    rcount.append(0)
    df=pd.DataFrame({'receipt_count':rcount,'date':dates})
    prepareData(df)
    df['month'] = df['month'] + 12
    df['month'] = df['month'] + 12
    df.loc[2:, 'weekofyear'] = df.loc[2:, 'weekofyear'] + 52
    sdf=scaler.transform(df)
    print(sdf)
    print(df)
    eval_batch=np.array(sdf[:7])
    current_batch = eval_batch.reshape((1, 7, 6))
    print(current_batch)
    pred=model.predict(current_batch)
    print(pred)
    sdf[7][0]=pred
    revdf=scaler.inverse_transform(sdf)
    print(revdf)
    return jsonify({'message': 'Data received successfully','nextCount':revdf[-1][0]})

if __name__ == '__main__':
    app.run(debug=True)
