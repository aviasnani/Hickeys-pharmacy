from flask import Blueprint, request, jsonify, make_response, session
from extensions import bcrypt, db
from models.admin import Admin
from models.staff import Staff
from flask_login import login_user, logout_user, current_user, login_required

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/admin_signup', methods=['POST'])
def admin_signup():
    req = request.get_json()
    print("Data has been received", req)
    secret_key = 'Badbunny!31'
    if req['secret_key'] != secret_key:
        return jsonify({"error": "Invalid secret key"}), 400
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

@admin_bp.route('/admin_login', methods=['POST'])
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
    
@admin_bp.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    try:  # added a try block to check whether the user logged in is an admin or not (co-pilot)
        # First verify this is an admin user
        if not isinstance(current_user, Admin):
            logout_user()
            return jsonify({"error": "Unauthorized access"}), 403
        staff_data = Staff.query.all()
        staff_list = []
        for staff in staff_data:
            staff_list.append({
            "id": staff.id,
            "fname": staff.fname,
            "lname": staff.lname,
            "age": staff.age,
            "phone": staff.phone,
            "dob": staff.dob,
            "username": staff.username,
        })
    
        return jsonify({
        "staff": staff_list,
        "admin_name": f'{current_user.fname} {current_user.lname}',
    }), 200
    except Exception as e: #throws an internal server error if the user is not authorized (co-pilot)
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
  

@admin_bp.route('/search_staff', methods=['POST'])
def search_staff():
    req = request.get_json()
    staff_people = Staff.query.filter(Staff.fname.ilike(req['fname'])).all()
    staff_list = []
    if staff_people:
        for staff in staff_people:
            staff_list.append({
                'id': staff.id,
                'fname': staff.fname,
                'lname': staff.lname,
                'age': staff.age,
                'phone': staff.phone,
                'dob': staff.dob,
                'username': staff.username
            })
        return jsonify(staff_list), 200

@admin_bp.route('/add_staff', methods=['POST'])
@login_required
def add_staff(): # this function does the same thing as the staff_signup function but is used to add staff from the admin dashboard
    if not isinstance(current_user, Admin):
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        req = request.get_json()
        existing_username = Staff.query.filter_by(username=req['username']).first()
        existing_phone = Staff.query.filter_by(phone=req['phone']).first()
        if existing_username:
            return jsonify({"error": "Username already exists. Please choose a different one."}), 400
        if existing_phone:
            return jsonify({"error": "Phone number already exists. Please choose a different one."}), 400
        if len(req['phone']) < 9:
            return jsonify({"error": "Phone number must be 10 digits long"}), 400
        if req['password'] != req['confirm_password']:
            return jsonify({"error": "Passwords do not match"}), 400
        hashed_password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
        new_staff = Staff( 
            fname=req['fname'],
            lname=req['lname'],
            age=req['age'],
            phone=req['phone'],
            dob=req['dob'],
            username=req['username'],
            password= hashed_password
        )
        db.session.add(new_staff)
        db.session.commit()
        return jsonify({"message": "Staff added successfully"}), 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/update_staff', methods=['PUT'])
def update_staff():
    if not isinstance(current_user, Admin):
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        req = request.get_json()
        print("Data has been received", req)
        staff = Staff.query.get(req['id'])
        if staff:
            staff.fname = req['fname']
            staff.lname = req['lname']
            staff.age = req['age']
            staff.phone = req['phone']
            staff.dob = req['dob']
            staff.username = req['username']
            db.session.commit()
            return jsonify({"message": "Staff updated successfully"}), 200
        else:
            return jsonify({"error": "Staff not found"}), 404
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/delete_staff', methods=['DELETE'])
def delete_staff():
    try:
        req =  request.get_json()
        staff_id = req['id']
        staff = Staff.query.filter_by(id=staff_id).first()
        if staff:
            db.session.delete(staff)
            db.session.commit()
            return jsonify({"message": "Staff deleted successfully"}), 200
        else:
            return jsonify({"error": "Staff not found"}), 404
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
  
@login_required
@admin_bp.route('/admin_logout')
def admin_logout():
    logout_user()
    print("User logged out")
    return jsonify({"message": "Logout successful"}), 200