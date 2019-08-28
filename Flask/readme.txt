how to upload to google(Google app engine)


download google sdk
create folder
name folder
add app.yaml file
*********************************
runtime: python27
#version: 1 #would give an error so remove it when deploying to google
api_version: 1
threadsafe: true

handlers: 
- url: /.*
  script: main.app

libraries:
- name: ssl
  version: latest

*************************

add appengine_config.py file
***************************
from google.appengine.ext import vendor
vendor.add('lib')

****************************

add main.py file
***************************
from flask import Flask
# app = Flask(__name__)
app = Flask("any_name")

@app.route('/')
def hello_world():
    return 'Hello Monkey!'

@app.route('/home')
def hello():
    return 'Hello Home!'

app.run(debug = True)
*****************************

add requirements file to host dependencies

create virtual environment for python2.7(preferrably with anaconda)
install dependencies in requirements file to lib file specified in appengine_config file

$ pip install -r requirements.txt -t lib

run app.yaml file
$ dev_appserver.py app.yaml

create new project in google cloud 

type in project directory(terminal)
authenticate in google cloud
$ gcloud auth application-default login

setting up the eliteweb app created in google cloud
$ gcloud config set project eliteweb

initializing the gcloud 
$ gcloud init

deploying the app 
$ gcloud app deploy app.yaml


#####################################################
when making updates
open virtual env from anaconda
go to project directory
run 
$ dev_appserver.py app.yaml

edit code

deploy again
$ gcloud app deploy app.yaml

######################################################



