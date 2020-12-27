from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
#from application.app.folder.file import func_name
from models.User import UserIn, UserOutClean
from DAL.user_DAL import user_DAL

# configuration
DEBUG = True
ROOT_PATH = "/stattracker/api/v1"

#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
jwt_confif = {
    "SECRET_KEY": "e41f43bcf9af08116d93df5d74f56cfd4b9a39584073a3bf44f216ce729c210a",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30
}

app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{ROOT_PATH}/users", response_model=List[UserOutClean])
async def get_all_users():
    users = user_DAL.get_all_users()
    if users == None:
        raise HTTPException(status_code=404, detail="No Users")
    return users

@app.get(f"{ROOT_PATH}/users/{{user_id}}", response_model=UserOutClean, response_model_exclude_unset=False)
async def get_user_by_id(user_id: int):
    user = user_DAL.get_user_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user