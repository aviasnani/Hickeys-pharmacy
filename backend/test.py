from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "patient_login" 

def unauthorized_handler(): # co-pilot 
    if request.path.startswith('/admin'):
        login_manager.login_view = 'admin_login'
    else:
        login_manager.login_view = 'patient_login'
    return jsonify({"error": "Please log in"}), 401
login_manager.unauthorized_handler(unauthorized_handler)

CORS(app, origins=["http://127.0.0.1:3000", "http://192.168.1.15:3000"], supports_credentials=True) # 

bcrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__)) # (co-pilot)
instance_path = os.path.join(basedir, 'instance') # (co-pilot)
if not os.path.exists(instance_path): # (co-pilot)
    os.makedirs(instance_path) # (co-pilot) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning
app.config['SECRET_KEY'] = 'Iaminevitable'
db = SQLAlchemy(app) 

@login_manager.user_loader
def load_user(user_id):
    role = session.get('role')
    if role == 'admin':
        return Admin.query.filter_by(id=int(user_id)).first()
    elif role == 'patient':
        return Patient.query.filter_by(id=int(user_id)).first()
    return None

login_manager.user_loader(load_user)

class Patient(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)



'''@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/patient_signup')
def patient_signup():
    return render_template('patient_signup.html')'''

@app.route('/admin_signup', methods=['POST'])
def admin_signup():
    req = request.get_json()
    print("Data has been received", req)
    res = make_response(jsonify(req), 200)
    existing_username = Admin.query.filter_by(username=req['username']).first() # queries the database for the username and checks if the entered username matches any of the usernames in the database
    if existing_username:
        return jsonify({"error": "Username already exists. Please choose a different one."}), 400
    existing_email = Admin.query.filter_by(email=req['email']).first()
    if existing_email:
        return jsonify({"error": "Email already exists. Please choose a different one."}), 400
    if req['password'] != req['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400
    hashed_password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
    new_admin = Admin(
        fname=req['first_name'],
        lname=req['last_name'],
        email=req['email'],
        username=req['username'],
        password=hashed_password
    )
    db.session.add(new_admin)
    db.session.commit()
    return res

@app.route('/patient_signup', methods=['POST'])
def patient_details():
    req = request.get_json() # get the data from the object where the form details are stored in js and convert it to python dictionary
    existing_username = Patient.query.filter_by(username=req['username']).first()
    if existing_username:
        return jsonify({"error": "Username already exists. Please choose a different one."}), 400
    existing_phone = Patient.query.filter_by(phone=req['phone_number']).first()
    if existing_phone:
        return jsonify({"error": "Phone number already exists. Please choose a different one."}), 400
    if len(req['phone_number']) < 9:
        return jsonify({"error": "Phone number must be 10 digits long"}), 400
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


@app.route('/patient_login', methods=['POST'])
def patient_login_details():
    req = request.get_json()
    print("Data has been received",req)
    existing_patient = Patient.query.filter_by(username=req['username']).first()
    if existing_patient and bcrypt.check_password_hash(existing_patient.password, req['password']):
        login_user(existing_patient)  # This is crucial
        session['role'] = 'patient'  # co-pilot
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401 

@login_required
@app.route('/patient_dashboard')
def patient_dashboard():
    try:  # added a try block to check whether the user logged in is an admin or not (co-pilot)
        # First verify this is an admin user
        if not isinstance(current_user, Patient):
            logout_user()
            return jsonify({"error": "Unauthorized access"}), 403
        
        return jsonify({
        "patient_name": f'{current_user.fname} {current_user.lname}',
        "patient_age": current_user.age,
        "patient_phone": current_user.phone,
        "patient_dob": current_user.dob,
        "patient_username": current_user.username,
    }), 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

@login_required
@app.route('/patient_logout')
def patient_logout():
    logout_user()
    print("User logged out")
    return jsonify({"message": "Logout successful"}), 200

@app.route('/admin_login', methods=['POST'])
def admin_login():
    req = request.get_json()
    print("Data has been received", req)
    existing_admin = Admin.query.filter_by(username=req['username']).first()
    if existing_admin and bcrypt.check_password_hash(existing_admin.password, req['password']):
         print(f"Admin authenticated: {existing_admin.fname} {existing_admin.lname}")
         print(f"Admin ID: {existing_admin.id}")
         login_user(existing_admin)  # This is crucial
         session['role'] = 'admin' # co-pilot
         return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    try:  # added a try block to check whether the user logged in is an admin or not (co-pilot)
        # First verify this is an admin user
        if not isinstance(current_user, Admin):
            logout_user()
            return jsonify({"error": "Unauthorized access"}), 403
        patient_data = Patient.query.all()
        patients = []
        for patient in patient_data:
            patients.append({
            "id": patient.id,
            "fname": patient.fname,
            "lname": patient.lname,
            "age": patient.age,
            "phone": patient.phone,
            "dob": patient.dob,
            "username": patient.username,
        })
    
        return jsonify({
        "patients": patients,
        "admin_name": f'{current_user.fname} {current_user.lname}',
    }), 200
    except Exception as e: #throws an internal server error if the user is not authorized (co-pilot)
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
        

@login_required
@app.route('/admin_logout')
def admin_logout():
    logout_user()
    print("User logged out")
    return jsonify({"message": "Logout successful"}), 200

with app.app_context():
        db.create_all()     

if __name__ == '__main__':
    app.run(debug=True)