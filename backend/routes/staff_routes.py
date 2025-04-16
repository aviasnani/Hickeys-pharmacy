from flask import Blueprint, request, jsonify, make_response, session
from models.staff import Staff
from extensions import bcrypt, db
from models.med import Meds
from flask_login import login_user, logout_user, current_user, login_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff_signup', methods=['POST'])
def staff_details():
    req = request.get_json() # get the data from the object where the form details are stored in js and convert it to python dictionary
    existing_username = Staff.query.filter_by(username=req['username']).first()
    if existing_username:
        return jsonify({"error": "Username already exists. Please choose a different one."}), 400
    existing_phone = Staff.query.filter_by(phone=req['phone_number']).first()
    if existing_phone:
        return jsonify({"error": "Phone number already exists. Please choose a different one."}), 400
    if len(req['phone_number']) < 9:
        return jsonify({"error": "Phone number must be 10 digits long"}), 400
    print("Data has been received",req) # print the data retrieved from the object
    res = make_response(jsonify(req), 200) # send a response back to the object
    if req['password'] != req['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400
    hashed_password = bcrypt.generate_password_hash(req['password']).decode('utf-8')
    new_staff = Staff( 
        fname=req['first_name'],
        lname=req['last_name'],
        age=req['age'],
        phone=req['phone_number'],
        dob=req['date_of_birth'],
        username=req['username'],
        password= hashed_password
)
    db.session.add(new_staff)
    db.session.commit()
    return res

@staff_bp.route('/staff_login', methods=['POST'])
def staff_login_details():
    req = request.get_json()
    print("Data has been received",req)
    existing_staff = Staff.query.filter_by(username=req['username']).first()
    if existing_staff and bcrypt.check_password_hash(existing_staff.password, req['password']):
        login_user(existing_staff)  # This is crucial
        session['role'] = 'staff'  # co-pilot
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401 

@login_required
@staff_bp.route('/staff_dashboard')
def staff_dashboard():
    try:  # added a try block to check whether the user logged in is an admin or not (co-pilot)
        # First verify this is an admin user
        if not isinstance(current_user, Staff):
            logout_user()
            return jsonify({"error": "Unauthorized access"}), 403
        staff_people = Staff.query.all()
        staff_list = []
        for staff in staff_people:
            staff_list.append({
                "id": current_user.id,
                "fname": current_user.fname,
                "lname": current_user.lname,
                "age": current_user.age,
                "phone": current_user.phone,
                "dob": current_user.dob,
                "username": current_user.username,
            })
        meds = Meds.query.all()
        med_list = []
        for med in meds:
            med_list.append({
                "id": med.id,
                "name": med.name,
                "brand": med.brand,
                "description": med.description,
                "form": med.form,
                "dosage": med.dosage,
                "price": med.price
            })
        
        return jsonify({
        "staff_name": current_user.fname + current_user.lname,
        "med": med_list
    }), 200
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
    
@staff_bp.route('/add_meds', methods=['POST'])
def add_meds():
    if not isinstance(current_user, Staff):
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        req = request.get_json()
        print("Data has been received", req)
        new_meds = Meds(
            name=req['name'],
            brand=req['brand'],
            description=req['description'],
            form=req['form'],
            dosage=req['dosage'],
            price=req['price']
        )
        db.session.add(new_meds)
        db.session.commit()
        return jsonify({"message": "Medicine added successfully"}), 200
    except Exception as e:  # added a try block to check whether the user logged in is an admin or not 
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
    
@staff_bp.route('/search_meds', methods=['POST'])
def search_meds():
    req = request.get_json()
    meds = Meds.query.filter(Meds.name.ilike(req['name'])).all()
    med_list = []
    if meds:
        for med in meds:
            med_list.append({
                'id': med.id,
                'name': med.name,
                'brand': med.brand,
                'description': med.description,
                'form': med.form,
                'dosage': med.dosage,
                'price': med.price
            })
        return jsonify(med_list), 200

@staff_bp.route('/edit_meds', methods=['PUT'])
def edit_meds():
    if not isinstance(current_user, Staff):
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        req = request.get_json()
        print("Data has been received", req)
        meds = Meds.query.get(req['id'])
        if meds:
            meds.name = req['name']
            meds.brand = req['brand']
            meds.description = req['description']
            meds.form = req['form']
            meds.dosage = req['dosage']
            meds.price = req['price']
            db.session.commit()
            return jsonify({"message": "Medicine edited successfully"}), 200
        else:
            return jsonify({"error": "Medicine not found"}), 404
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


@staff_bp.route('/delete_meds', methods=['DELETE']) # works same as delete staff 
def delete_meds():
    try:
        req = request.get_json()
        med_id = req['id']
        med = Meds.query.filter_by(id=med_id).first()
        if med:
            db.session.delete(med)
            db.session.commit()
            return jsonify({"message": "Medicine deleted successfully"}), 200
        else:
            return jsonify({"error": "Medicine not found"}), 404
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

@login_required
@staff_bp.route('/staff_logout')
def staff_logout():
    logout_user()
    print("User logged out")
    return jsonify({"message": "Logout successful"}), 200