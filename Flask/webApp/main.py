from flask import Flask
# app = Flask(__name__)
app = Flask("any_name")

@app.route('/')
def main():
    return 'What is happening?!'

@app.route('/home')
def home():
    return 'Hello Home!'

#app.run(debug = True)
