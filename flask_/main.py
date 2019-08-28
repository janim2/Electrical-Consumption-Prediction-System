# from flask import Flask, render_template, redirect, request
# # app = Flask(__name__)
# app = Flask("any_name")

# thename = "Jesse"
# theage = 50
# basket = ["mango","banana","orange","apple"]
# thesubject = ["amath","bmath","smath","jenglish"]

# @app.route('/', methods=['GET','POST'])
# def hello_world():
#     if request.method == 'POST':
#         value = request.form.get('val')
#         # return redirect('/home')
#         return render_template('index.html',txt=value)

#     return render_template("index.html",name=thename,age=theage,
#     items=basket,subjects=thesubject)

# @app.route('/home', methods=['GET','POST'])
# def home():
#     if request.method == 'POST':
#         return redirect('/')
#     return render_template("second.html")

# @app.route('/profile', methods=['GET','POST'])
# def profile():
#     return 'Hello Profile!'

# app.run(debug = True)



#*****************************************************************
#simple calculator app in flask

# importing the modules we will use

# from flask import Flask, request, render_template

# # naming our app
# app = Flask("Calculator")

# """
# In this section of the code, we will create our functions to perform the operations
# Each function takes 2 parameters - which are the numbers you will collect from the HTML form

# """

# # in portions of the code where there are 3 quotation marks in a row, you have to fill in the code eg. """ """
# def add(a, b):
# 	# function to add 2 numbers
# 	return int(a) + int(b)

# def subtract(a, b):
# 	# function to subtract 2 numbers
# 	return int(a) - int(b)

# def divide(a, b):
# 	# function to divide 2 numbers
# 	return int(a) / int(b)

# def multiply(a, b):
# 	# function to multiply 2 numbers
# 	return int(a) * int(b)

# @app.route('/', methods=['GET','POST'])
# def page():
# 	if request.method == 'POST':
# 		if request.form.get("add_button") == "Add":
# 			return render_template("index.html", answer=add(request.form.get("first"), request.form.get("second")))
# 		elif request.form.get("subtract_button") == "Subtract":
# 			return render_template("index.html", answer=subtract(request.form.get("first"),request.form.get("second")))
# 		elif request.form.get("divide_button") == "Divide":
# 			return render_template("index.html", answer=divide(request.form.get("first"),request.form.get("second")))
# 		else:
# 			return render_template("index.html", answer=multiply(request.form.get("first"),request.form.get("second")))
# 	else:
# 		return render_template("index.html")

# app.run(debug=True)



#**************************************************************
#adding values entered from editext into a list

#from flask import Flask, render_template, redirect, request
# app = Flask(__name__)
#app = Flask("any_name")

#the_persons = []


#@app.route('/lists', methods=['GET','POST'])
#def hello_world():
#    if request.method == 'POST':
#        # return redirect('/home')
#    
#        the_persons.append(request.form.get('theperson'))
#        return render_template('lists.html',the_p=the_persons)
    
#    return render_template('lists.html',the_p=the_persons)

#app.run(debug=True)


#***********************************************************
#rendering a child page into a parent page called base.html
from flask import Flask, render_template, redirect, request, url_for
# app = Flask(__name__)
app = Flask("any_name")

# In this section of the code, we will create our functions to perform the operations
# Each function takes 2 parameters - which are the numbers you will collect from the HTML form

# """

# # in portions of the code where there are 3 quotation marks in a row, you have to fill in the code eg. """ """
def add(a, b):
    # function to add 2 numbers
    return int(a) + int(b)

def subtract(a, b):
    # function to subtract 2 numbers
    return int(a) - int(b)

def divide(a, b):
    # function to divide 2 numbers
    return int(a) / int(b)

def multiply(a, b):
    # function to multiply 2 numbers
    return int(a) * int(b)


the_persons = []


@app.route('/base', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        # return redirect('/home')
    
        the_persons.append(request.form.get('theperson'))
        return render_template('base.html',the_p=the_persons)
    
    return render_template('base.html',the_p=the_persons)

@app.route('/lists', methods=['GET','POST'])
def lists():
    if request.method == 'POST':
        # return redirect('/home')
    
        the_persons.append(request.form.get('theperson'))
        return render_template('lists.html',the_p=the_persons)
    
    return render_template('lists.html',the_p=the_persons)
	
@app.route('/', methods=['GET','POST'])
def page():
 	if request.method == 'POST':
 		if request.form.get("add_button") == "Add":
 			return render_template("index.html", answer=add(request.form.get("first"), request.form.get("second")))
 		elif request.form.get("subtract_button") == "Subtract":
 			return render_template("index.html", answer=subtract(request.form.get("first"),request.form.get("second")))
 		elif request.form.get("divide_button") == "Divide":
 			return render_template("index.html", answer=divide(request.form.get("first"),request.form.get("second")))
 		else:
 			return render_template("index.html", answer=multiply(request.form.get("first"),request.form.get("second")))
 	else:
 		return render_template("index.html")
	
app.run(debug=True)
