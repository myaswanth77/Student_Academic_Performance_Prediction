import numpy as np
from flask import Flask, request, jsonify, render_template,redirect,url_for
import pickle
import model
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

# Create flask app
flask_app = Flask(__name__)
# flask_app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:test123@localhost:5432/sapp_db'
# db=SQLAlchemy(flask_app)

# class Login(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)

# class Registration(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     rollno = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)


# # Create database tables
# with flask_app.app_context():
#     db.create_all()


model = pickle.load(open("sapp_final_algo.pkl", "rb"))

@flask_app.route("/")
def home():
    return render_template("start.html")

# @flask_app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == "POST" and "name" in request.form and "rollno" in request.form and "email" in request.form and "password1" in request.form and "password2" in request.form:
#         name = request.form['name']
#         rollno = request.form['rollno']
#         email = request.form['email']
#         password1 = request.form['password1']
#         password2 = request.form['password2']
#         if password1 == password2:
#             new_registration = Registration(name=name, rollno=rollno, email=email, password=password1)
#             db.session.add(new_registration)
#             db.session.commit()
#             return "Registration data added to database"
#         else:
#             return "Passwords do not match"
#     return render_template("register.html")




# @flask_app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "POST" and "username" in request.form and "password" in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         new_login = Login(username=username, password=password)
#         db.session.add(new_login)
#         db.session.commit()
#         return "Login data added to database"
#     return render_template("login.html")






@flask_app.route("/grade")
def index():
    return render_template("grade.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    data = {
    'RollNo': request.form['rollno'],
    'Gender': request.form['gender'],
    'Age': request.form['age'],
    'Location': request.form['location'],
    'Famsize': request.form['famsize'],
    'Pstatus': request.form['pstatus'],
    'Medu': request.form['medu'],
    'Fedu': request.form['fedu'],
    'Mjob': request.form['mjob'],
    'Fjob': request.form['fjob'],
    'reason': request.form['reason'],
    'traveltime': request.form['traveltime'],
    'studytime': request.form['studytime'],
    'Failures': request.form['backlogs'],
    'Famsup': request.form['famsup'],
    'Paid': request.form['paid'],
    'Activities': request.form['activities'],
    'HigherEdu': request.form['higheredu'],
    'Internet': request.form['internet'],
    'Famrel': request.form['famrel'],
    'Freetime': request.form['freetime'],
    'GoOut': request.form['goout'],
    'Health': request.form['health'],
    '10th%': request.form['10thpercent'],
    '12thordiploma%': request.form['12thordiploma%'],
    'Internal': request.form['internals'],
    'Prev cgpa': request.form['sgpa'],

    'Total_eamcet/ecet_grade': 0  }
    if request.form['entrance'] == 'Eamcet':
        data['Eamcet Rank'] = request.form['entrance_rank']
        data['Ecet Rank']=0
    elif request.form['entrance'] == 'Ecet':
        data['Eamcet Rank']=0
        data['Ecet Rank'] = request.form['entrance_rank']
 
    input_df = pd.DataFrame([data], columns=data.keys())

    prediction = model.predict(input_df)

    output = {"prediction": round(prediction[0], 2)}

    prediction_text = "Predicted Grade is " + str(output["prediction"])
    return redirect(url_for("result", prediction_text=prediction_text))

@flask_app.route("/result")
def result():
    prediction_text = request.args.get("prediction_text")
    return render_template("result.html", prediction_text=prediction_text)

if __name__ == "__main__":
    flask_app.run(debug=True)
