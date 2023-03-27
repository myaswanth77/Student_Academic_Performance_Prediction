import numpy as np
from flask import Flask, request, jsonify, render_template,redirect,url_for,flash
import pickle
import model
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


# Create flask app
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sapp123@localhost:5432/sapp_db'
flask_app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(flask_app)

# Create login manager
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)  
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    age = db.Column(db.Integer)
    location = db.Column(db.String(255))
    famsize = db.Column(db.String(255))
    pstatus = db.Column(db.String(255))
    medu = db.Column(db.String(255))
    fedu = db.Column(db.String(255))
    mjob = db.Column(db.String(255))
    fjob = db.Column(db.String(255))
    reason = db.Column(db.String(255))
    traveltime = db.Column(db.String(255))
    studytime = db.Column(db.String(255))
    failures =db.Column(db.Integer)
    famsup = db.Column(db.String(255))
    paid = db.Column(db.String(255))
    activities = db.Column(db.String(255))
    higheredu = db.Column(db.String(255))
    internet = db.Column(db.String(255))
    famrel =db.Column(db.String(255))
    freetime = db.Column(db.String(255))
    goout = db.Column(db.String(255))
    health = db.Column(db.String(255))
    tenth_percent = db.Column(db.Float)
    twelfth_percent = db.Column(db.Float)
    internals = db.Column(db.Float)
    sgpa = db.Column(db.Float)
    entrance_exam = db.Column(db.String(255))
    entrance_rank = db.Column(db.Integer)
    predicted_grade = db.Column(db.Float)

    # def __repr__(self):
    #     print(repr(user_data))
    #     return f"UserData('{self.rollno}', '{self.predicted_grade}')"



# Define loader function for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/grade')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully')
            return redirect('/grade')
        else:
            flash('Invalid credentials')
            return redirect('/login')

    else:
        return render_template('login.html')
    
@flask_app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/grade')

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['rollno']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 == password2:
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect('/register')

            elif User.query.filter_by(email=email).first():
                flash('Email already exists')
                return redirect('/register')

            else:
                
                user = User(name=name, username=username, email=email, password=generate_password_hash(password1))
                db.session.add(user)
                db.session.commit()
                flash('User created')
                return redirect('/login')
        else:
            flash('Password is not matching')
            return redirect('/register')

    else:
        return render_template('register.html')



model = pickle.load(open("sapp_final_algo.pkl", "rb"))

@flask_app.route("/")
def home():
    return render_template("start.html")


@flask_app.route('/grade')
def grade():
    if not current_user.is_authenticated:
        return redirect('/login')

    return render_template('grade.html')

@flask_app.route("/predict", methods = ["POST"])
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

    new_data = UserData(rollno=data['RollNo'], gender=data['Gender'], age=data['Age'], location=data['Location'],
                            famsize=data['Famsize'], pstatus=data['Pstatus'], medu=data['Medu'], fedu=data['Fedu'], mjob=data['Mjob'],
                            fjob=data['Fjob'], reason=data['reason'], traveltime=data['traveltime'], studytime=data['studytime'],
                            failures=data['Failures'], famsup=data['Famsup'], paid=data['Paid'], activities=data['Activities'],
                            higheredu=data['HigherEdu'], internet=data['Internet'], famrel=data['Famrel'], freetime=data['Freetime'],
                            goout=data['GoOut'], health=data['Health'], tenth_percent=data['10th%'],
                            twelfth_percent=data['12thordiploma%'], internals=data['Internal'],sgpa=data['Prev cgpa'] ,
                            entrance_exam=request.form['entrance'], entrance_rank=request.form['entrance_rank'],
                            predicted_grade=str(output["prediction"])) 

    db.session.add(new_data)
    db.session.commit()


    

    prediction_text = "Predicted Grade is " + str(output["prediction"])
    return redirect(url_for("result", prediction_text=prediction_text))

@flask_app.route("/result")
def result():
    prediction_text = request.args.get("prediction_text")
    return render_template("result.html", prediction_text=prediction_text)

# Create database tables
with flask_app.app_context():
    db.create_all()



if __name__ == "__main__":
    flask_app.run(debug=True)
