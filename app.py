from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# Configure the MongoDB URI and initialize the PyMongo
app.config["MONGO_URI"] = "mongodb+srv://kgolatka:root@cluster0.vzbsfma.mongodb.net/personal_income_expense_tracker"

mongo = PyMongo(app)

@app.route('/signup', methods=['POST'])
def signup():
    # Extract the data from the request
    data = request.json
    first_name = data.get('FirstName')
    last_name = data.get('LastName')
    user_name = data.get('UserName')
    password = data.get('Password')

    # Check if all fields are provided
    if not first_name or not last_name or not user_name or not password:
        return jsonify({'error': 'Missing fields'}), 400

    # Check if the user already exists
    user = mongo.db.users_information.find_one({'UserName': user_name})
    if user:
        return jsonify({'error': 'Username already exists'}), 409

    # Store the user with plain text password (not recommended)
    mongo.db.users_information.insert_one({
        'FirstName': first_name,
        'LastName': last_name,
        'UserName': user_name,
        'Password': password  # Storing the password as plain text
    })
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Extract the data from the request
    data = request.json
    user_name = data.get('UserName')
    password = data.get('Password')

    # Check if both fields are provided
    if not user_name or not password:
        return jsonify({'error': 'Missing UserName or Password'}), 400

    # Find the user in the database
    user = mongo.db.users_information.find_one({'UserName': user_name})

    # Check the password
    if user and user['Password'] == password:
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/create_financials', methods=['POST'])
def create_financials():
    data = request.json
    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    # You might want to include further validation of the input data here

    # Insert the new financial document into the MongoDB collection
    inserted_id = mongo.db.users_financials.insert_one(data).inserted_id
    return jsonify({'message': 'Financial record created', 'inserted_id': str(inserted_id)}), 201



@app.route('/get_financials/<username>', methods=['GET'])
def get_financials(username):
    # Retrieve all financial documents for the user
    financials = mongo.db.users_financials.find({'username': username})
    return dumps(financials), 200

@app.route('/get_update_financials/<username>/<int:year>/<month>', methods=['GET'])
def get_update_financials(username,year,month):
    financials = mongo.db.users_financials.find({'username':username, 'year':year, 'month':month})
    return dumps(financials), 200

@app.route('/set_update_financials/<username>/<int:year>/<month>/<field>/<source>/<float:amount>', methods=['POST'])
def set_update_financials(username,year,month,field,source,amount):
    update_id = mongo.db.users_financials.update_one({'username':username, 'year':year, 'month':month},{"$set":{f"{field}.{source}":amount}})
    if(update_id.modified_count>0):
        return jsonify({'message': 'Financial record updated'}), 201
    
@app.route('/delete_financials/<username>/<int:year>/<month>', methods=['DELETE'])
def delete_financials(username, year, month):
    # Delete the financial record from the database
    result = mongo.db.users_financials.delete_one({'username': username, 'year': year, 'month': month})
    
    if result.deleted_count > 0:
        return jsonify({'message': 'Financial record deleted successfully'}), 200
    else:
        return jsonify({'error': 'No record found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 
