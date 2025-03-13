from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response


app = Flask(__name__)

@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/patient_signup')
def patient_signup():
    return render_template('patient_signup.html')



@app.route('/patient_signup/patient_details', methods=['POST'])
def patient_details():
    req = request.get_json() # get the data from the object where the form details are stored in js and convert it to python dictionary
    print("Data has been received",req) # print the data retrieved from the object
    res = make_response(jsonify(req), 200) # send a response back to the object
    return res


if __name__ == '__main__':
    app.run(debug=True)