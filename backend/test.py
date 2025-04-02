from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "patient_login" 

CORS(app, origins=["http://127.0.0.1:3000"], supports_credentials=True) # 

bcrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__)) # (co-pilot)
instance_path = os.path.join(basedir, 'instance') # (co-pilot)
if not os.path.exists(instance_path): # (co-pilot)
    os.makedirs(instance_path) # (co-pilot) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning
app.config['SECRET_KEY'] = 'Iaminevitable'
db = SQLAlchemy(app) 

def load_user(user_id):
    return Patient.query.get(int(user_id))

login_manager.user_loader(load_user)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)



'''@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/patient_signup')
def patient_signup():
    return render_template('patient_signup.html')'''



@app.route('/patient_signup', methods=['POST'])
def patient_details():
    req = request.get_json() # get the data from the object where the form details are stored in js and convert it to python dictionary
    print("Data has been received",req) # print the data retrieved from the object
    res = make_response(jsonify(req), 200) # send a response back to the object
    if req['password'] != req['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400
    hashed_password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
    new_patient = Patient( 
        fname=req['first_name'],
        lname=req['last_name'],
        age=req['age'],
        phone=req['phone_number'],
        dob=req['date_of_birth'],
        username=req['username'],
        password= hashed_password
)
    db.session.add(new_patient)
    db.session.commit()
    return res

'''@app.route('/patient_login')
def patient_login():
    return render_template('patient_login.html')'''

@app.route('/patient_login', methods=['POST'])
def patient_login_details():
    req = request.get_json()
    print("Data has been received",req)
    existing_patient = Patient.query.filter_by(username=req['username']).first()
    if existing_patient and bcrypt.check_password_hash(existing_patient.password, req['password']):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401 

'''@login_required
@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template('patient_dashboard.html')'''

@app.route('/patient_logout')
def patient_logout():
    logout_user()
    print("User logged out")
    return jsonify({"message": "Logout successful"}), 200

with app.app_context():
        db.create_all()     

if __name__ == '__main__':
    app.run(debug=True)