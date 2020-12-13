# https://gist.github.com/miguelgrinberg/5614326
# https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/

from flask import Flask, request, url_for
from flask_cors import CORS

from response_handler import ResponseHandler
from dal_user import DAL_user

# configuration
DEBUG = True
ROOT_PATH = "/stattracker/api/v1"

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def requestJsonPropInvalid(request, prop):
    return not prop in request.json or not request.json[prop]

# Routes
# Users
####################################################
@app.route(f'{ROOT_PATH}/users', methods=['GET'])
def get_users():
    users = DAL_user.get_all_users()
    for user in users:
        del user["password"]
        del user["dob"]
        del user["gender"]
    return ResponseHandler(users).jsonify()

@app.route(f'{ROOT_PATH}/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = DAL_user.get_user_by_id(user_id)
    if user:
        del user["password"]
        del user["dob"]
        del user["gender"]
        return ResponseHandler(user).jsonify()
    else:
        return ResponseHandler(errorMessage = "Record not found").jsonify()

@app.route(f'{ROOT_PATH}/authenticate', methods=['POST'])
def authenticate():
    if not request.json:
        return ResponseHandler(errorMessage = "Object not submitted").jsonify()
    if requestJsonPropInvalid(request, 'email'): 
        return ResponseHandler(errorMessage = "Username cannot be empty").jsonify()
    if requestJsonPropInvalid(request, 'password'): 
        return ResponseHandler(errorMessage = "Password cannot be empty").jsonify()

    user = DAL_user.validate_user(userId=request.json['userId'], email=request.json['email'], password=request.json['password'])
    if user:
        del user["password"]        
        # Create Token
        # Until Then
        return ResponseHandler(user).jsonify()
    else:
        return ResponseHandler(errorMessage = "Incorrect username or password").jsonify()
    


    # authUser = {
    #     'username': request.json['username'],
    #     'roles': ['Admin']
    #     # 'class': request.json.get('class', False)
    # }

# @app.route(f'{ROOT_PATH}/students', methods=['POST'])
# def save_student():
#     if not request.json:
#         return ResponseHandler(errorMessage = "No data submitted").toJSON(), 200
#     if not 'firstname' in request.json or not request.json['firstname']:
#         return ResponseHandler(errorMessage = "Firstname cannot be empty").toJSON(), 200
#     if not 'lastname' in request.json or not request.json['lastname']:
#         return ResponseHandler(errorMessage = "Lastname cannot be empty").toJSON(), 200
#     if not 'class' in request.json or not request.json['class']:
#         return ResponseHandler(errorMessage = "Class cannot be empty").toJSON(), 200
#     student = {
#         'id': students[-1]['id'] + 1,
#         'firstName': request.json['firstName'],
#         'lastName': request.json('lastName'),
#         'class': request.json('class'),
#         # 'class': request.json.get('class', False)
#     }
#     students.append(student)
#     return ResponseHandler(student).toJSON()
####################################################

if __name__ == '__main__':
    app.run()