# https://gist.github.com/miguelgrinberg/5614326
# https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/

from flask import Flask, request, url_for, jsonify
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
def get_students():
    users = DAL_user.get_all_users()
    for user in users:
        print(type(user))
        print(user)
        del user["dob"]
        del user["password"]

    return jsonify(ResponseHandler(users).to_dict())

# @app.route(f'{ROOT_PATH}/students/<int:task_id>', methods=['GET'])
# def get_student(task_id):
#     student = list(filter(lambda t: t['id'] == task_id, students))
#     if len(student) == 0:
#         return ResponseHandler(errorMessage = "Record not found").toJSON()
#     return ResponseHandler(payload=student[0]).toJSON()

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

# @app.route(f'{ROOT_PATH}/authenticate', methods=['POST'])
# def authenticate():
#     if not request.json:
#         return ResponseHandler(errorMessage = "Object not submitted").to_JSON()
#     if requestJsonPropInvalid(request, 'username'): 
#         return ResponseHandler(errorMessage = "Username cannot be empty").to_JSON()
#     if requestJsonPropInvalid(request, 'password'): 
#         return ResponseHandler(errorMessage = "Password cannot be empty").to_JSON()

#     authUser = {
#         'username': request.json['username'],
#         'roles': ['Admin']
#         # 'class': request.json.get('class', False)
#     }

#     return ResponseHandler(authUser).to_JSON(), 200

if __name__ == '__main__':
    app.run()