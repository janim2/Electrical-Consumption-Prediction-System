from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_socketio import SocketIO, emit
import random
import urllib.request
from werkzeug.utils import secure_filename
import os
from model import Database

# load and clean-up data
from numpy import nan
from numpy import isnan
from pandas import read_csv
from pandas import to_numeric
from math import sqrt

from numpy import split
from numpy import array
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

isDone = False
app = Flask("any_name")
socketio = SocketIO(app)
# firebase = firebase.FirebaseApplication('https://eliteweb.firebaseio.com',None)
# firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)

UPLOAD_FOLDER = '/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        ttemail = request.form.get('email')
        tpassword = request.form.get('password')
        db = Database()
        if db.isUserValid(ttemail, tpassword):
            return redirect("/dashboard")
        render_template('Login.html')
    return render_template('Login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    db = Database()
    if request.method == 'POST':
        fullname = request.form.get('fulllname')
        email = request.form.get('the_email')
        phone_number = request.form.get('the_phone_number')
        password = request.form.get('password')
        confirmpass = request.form.get('confirm_pass')
        if password != "" and confirmpass != "" and password == confirmpass:
            db.insertUser(fullname, email, password)
            print("done")
            # return render_template('Register.html',errormessage="User added successfully")
            return redirect('/')
        return render_template('Register.html',errormessage="Mismatch password")
    return render_template('Register.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    if request.method =='POST':
        file = request.files['file[]']
        if file:
            filename = secure_filename(file.filename)
            # filename = 'household_power_consumption'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # render_template('dashboard.html',load='../static/images/loading.gif')

            # '/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/static/images/new_plot.png')
            # StartPredication('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files')
            # fill missing values with a value at the same time one day ago
            
            fileloaction = "/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files"
            # load all data
            dataset = read_csv(fileloaction+"/read.txt", sep=';', header=0, low_memory=False, infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])
            # mark all missing values
            dataset.replace('?', nan, inplace=True)
            # make dataset numeric
            dataset = dataset.astype('float32')
            # fill missing
            fill_missing(dataset.values)
            # add a column for for the remainder of sub metering
            values = dataset.values
            dataset['sub_metering_4'] = (values[:,0] * 1000 / 60) - (values[:,4] + values[:,5] + values[:,6])
            # save updated dataset
            dataset.to_csv('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files/household_power_consumption.csv')
            
            # load the new file
            dataset = read_csv('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files/household_power_consumption.csv', header=0, infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
            # resample data to daily
            daily_groups = dataset.resample('D')
            daily_data = daily_groups.sum()
            # summarize
            print(daily_data.shape)
            print(daily_data.head())
            # save
            daily_data.to_csv('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files/household_power_consumption_days.csv')
            
            # load the new file
            dataset = read_csv('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/files/household_power_consumption_days.csv', header=0, infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
            
            # split into train and test
            train, test = split_dataset(dataset.values)

            # define the names and functions for the models we wish to evaluate
            models = dict()
            models['arima'] = arima_forecast
            # evaluate each model
            days = ['sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat']
            for name, func in models.items():
                # evaluate and get scores
                score, scores = evaluate_model(func, train, test)
                # summarize scores
                summarize_scores(name, score, scores)
                print(days,scores)
                # plot scores
                pyplot.plot(days, scores, marker='o', label=name)
                pyplot.xlabel('Days', fontsize=18)
                pyplot.ylabel('Power Consumption (kWh)', fontsize=16)
                # pyplot.savefig('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/static/images/new_plot.png')

            isDone = False
            pyplot.savefig('/home/jesse/Documents/Machine Learning/ELITE/PROJECT/website/static/images/new_plot.png')
            isDone = True
            return render_template('dashboard.html',finised=True,theday=days,thescore=scores)
    return render_template('dashboard.html')


@app.route('/notifications')
def notifications():
    return render_template("notifications.html")

@app.route('/profile')
def profile():
    return render_template("user.html")

@app.route('/stats')
def stats():
    return render_template("tables.html")


@app.route('/image_generated')
def checkImage():
    if (isDone):
        return 'true'
    return ('false')



# def registerUser(thefname,theemail,thepnumber, thepass):
#     pass

def fill_missing(values):
    one_day = 60 * 24
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            if isnan(values[row, col]):
                values[row, col] = values[row - one_day, col]

def evaluate_forecasts(actual, predicted):
    scores = list()
    # calculate an RMSE score for each day
    for i in range(actual.shape[1]):
        # calculate mse
        mse = mean_squared_error(actual[:, i], predicted[:, i])
        # calculate rmse
        rmse = sqrt(mse)
        # store
        scores.append(rmse)
    # calculate overall RMSE
    s = 0
    for row in range(actual.shape[0]):
        for col in range(actual.shape[1]):
            s += (actual[row, col] - predicted[row, col])**2
    score = sqrt(s / (actual.shape[0] * actual.shape[1]))
    return score, scores

# split a univariate dataset into train/test sets
def split_dataset(data):
    # split into standard weeks
    train, test = data[1:-328], data[-328:-6]
    # restructure into windows of weekly data
    train = array(split(train, len(train)/7))
    test = array(split(test, len(test)/7))
    print(test.shape)
    print(test)
    return train, test  

# convert windows of weekly multivariate data into a series of total power
def to_series(data):
    # extract just the total power from each week
    series = [week[:, 0] for week in data]
    # flatten into a single series
    series = array(series).flatten()
    return series

# evaluate a single model
def evaluate_model(model_func, train, test):
    # history is a list of weekly data
    history = [x for x in train]
    # walk-forward validation over each week
    predictions = list()
    for i in range(len(test)):
        # predict the week
        yhat_sequence = model_func(history)
        # store the predictions
        predictions.append(yhat_sequence)
        # get real observation and add to history for predicting the next week
        history.append(test[i, :])
    predictions = array(predictions)
    # evaluate predictions days for each week
    score, scores = evaluate_forecasts(test[:, :, 0], predictions)
    return score, scores

# summarize scores
def summarize_scores(name, score, scores):
    s_scores = ', '.join(['%.1f' % s for s in scores])
    print('%s: [%.3f] %s' % (name, score, s_scores))

# #convert windows of weekly multivariate data into a series of total power
# def to_series(data):
#     # extract just the total power from each week
#     series = [week[:, 0] for week in data]
#     # flatten into a single series
#     series = array(series).flatten()
#     return series

# arima forecast
def arima_forecast(history):
    # convert history into a univariate series
    series = to_series(history)
    # define the model
    model = ARIMA(series, order=(7,0,0))
    # fit the model
    model_fit = model.fit(disp=False)
    # make forecast
    yhat = model_fit.predict(len(series), len(series)+6)
    return yhat

def StartPredication(fileloaction):
    return render_template('dashboard.html',finised=True)

    # show plot
    #pyplot.legend()
    #pyplot.show()    

@app.route('/complete')
def complete():
    print(isDone)
    return jsonify(_success=isDone)

# @socketio.on('connect')
# def test_connect(data):
#     print (data)
#     emit('complete',  {'data':'Lets dance'})


app.run(debug = True)
