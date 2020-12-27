from fastapi import FastAPI
from typing import List

#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
#from application.app.folder.file import func_name
from models.User import UserIn, UserOutClean
from DAL.user_DAL import user_DAL

# configuration
DEBUG = True
ROOT_PATH = "/stattracker/api/v1"

app = FastAPI()

@app.get(f"{ROOT_PATH}/users", response_model=List[UserOutClean])
async def get_all_users():
    #return {"message": "Hello World"}

    users = user_DAL.get_all_users()
    print(users)

    # userOut = {
    #     "userId": 1,
    #     "email": "duanehaworth@hotmail.com",
    #     "firstname": "Duane",
    #     "lastname": "Haworth"
    # }

    return users

@app.get(f"{ROOT_PATH}/users/{{user_id}}", response_model=UserOutClean, response_model_exclude_unset=True)
async def get_user_by_id(user_id: int):
    #return {"message": "Hello World"}

    userOut = {
        "userId": user_id,
        "email": "duanehaworth@hotmail.com",
        "firstname": "Duane",
        "lastname": "Haworth"
    }

    return userOut    