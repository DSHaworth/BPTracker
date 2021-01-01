from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import List
import sqlite3

from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
#from application.app.folder.file import func_name
from models.User import UserLogon, UserCreateDto, UserOutClean
from models.Weight import WeightDto
from models.Pulse import PulseDto
from models.Bp import BpDto
#
from DAL.user_dal import user_DAL
from DAL.weight_dal import weight_DAL
from DAL.pulse_dal import pulse_DAL
from DAL.bp_dal import bp_DAL
#
from utils.pwd_helper import Pwd_Helper

# configuration
DEBUG = True
ROOT_PATH = "/stattracker/api/v1"

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

@app.post(f'{ROOT_PATH}/users', status_code=201) #201 = created
async def create_user(user: UserCreateDto):
    
    if user.password != user.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        user.password = Pwd_Helper.get_password_hash(user.password)
        user_DAL.add_user(user)
        return None
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail=f"'{user.email}' already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # validate_password = Pwd_Helper.verify_password(userCreate.password, hash_password)
    # print(validate_password)

@app.post(f'{ROOT_PATH}/authenticate')
async def authenticate(userLogon: UserLogon):
    
  user = user_DAL.validate_user(userLogon)
  if user:
    access_token_expires = timedelta(minutes=jwt_config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    weight_stats = weight_DAL.get_weights_by_user(user.userId)

    # print("access_token")
    # print(access_token)
    # print(user)
    return { 
        "token": access_token,
        "user": user,
        # {
        #     "access_token": access_token, 
        #     "token_type": "bearer"
        # },
        "weightStats": weight_stats
    }
    #return user

  raise HTTPException(status_code=401, detail=f"Logon failed")

##############################################
# AUTHENTICATION/TOKENS
##############################################
class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    email: str = None
    isActive: Optional[int] = None


#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
jwt_config = {
    "SECRET_KEY": "e41f43bcf9af08116d93df5d74f56cfd4b9a39584073a3bf44f216ce729c210a",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_user_by_email(email):
    user = user_DAL.get_user_by_email(email)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user  


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

  to_encode = data.copy()

  if expires_delta:
      expire = datetime.utcnow() + expires_delta
  else:
      expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, jwt_config["SECRET_KEY"], algorithm = jwt_config["ALGORITHM"])
  return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_config["SECRET_KEY"], algorithms=[jwt_config["ALGORITHM"]])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.email)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.isActive == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user  

##########################################
# Weight
##########################################
@app.get(f"{ROOT_PATH}/weightstats/{{user_id}}", response_model=List[WeightDto], response_model_exclude_unset=False)
async def get_weight_by_user(user_id: int, current_user: User = Depends(get_current_active_user)):
  weight_stats = weight_DAL.get_weights_by_user(user_id)
  if weight_stats == None:
      raise HTTPException(status_code=404, detail="User not found")
  return weight_stats

@app.post(f'{ROOT_PATH}/weightstats/{{user_id}}/{{weight_id}}', status_code=201) #201 = created
async def update_weight(user_id: int, weight_id: int, weight_dto: WeightDto, current_user: User = Depends(get_current_active_user)):
  try:
    weight_DAL.update_weight(weight_dto)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.delete(f'{ROOT_PATH}/weightstats/{{user_id}}/{{weight_id}}', status_code=201) #201 = created
async def delete_weight(user_id: int, weight_id: int, current_user: User = Depends(get_current_active_user)):
  try:
    weight_DAL.delete_weight(weight_id)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.post(f'{ROOT_PATH}/weightstats/', status_code=201) #201 = created
async def create_weight(weight_dto: WeightDto, current_user: User = Depends(get_current_active_user)):
  try:
    weight_DAL.add_weight(weight_dto)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

##########################################
# Pulse
##########################################
@app.get(f"{ROOT_PATH}/pulsestats/{{user_id}}", response_model=List[PulseDto], response_model_exclude_unset=False)
async def get_pulse_by_user(user_id: int, current_user: User = Depends(get_current_active_user)):
  pulse_stats = pulse_DAL.get_pulse_stats_by_user(user_id)
  if pulse_stats == None:
      raise HTTPException(status_code=404, detail="User not found")
  return pulse_stats

@app.post(f'{ROOT_PATH}/pulsestats/{{user_id}}/{{pulse_id}}', status_code=201) #201 = created
async def update_pulse_stat(user_id: int, pulse_id: int, pulse_dto: PulseDto, current_user: User = Depends(get_current_active_user)):
  try:
    pulse_DAL.update_pulse(pulse_dto)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.delete(f'{ROOT_PATH}/pulsestats/{{user_id}}/{{pulse_id}}', status_code=201) #201 = created
async def delete_pulse_stat(user_id: int, pulse_id: int, current_user: User = Depends(get_current_active_user)):
  try:
    pulse_DAL.delete_pulse(pulse_id)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.post(f'{ROOT_PATH}/pulsestats/', status_code=201) #201 = created
async def create_pulse(pulse_dto: PulseDto, current_user: User = Depends(get_current_active_user)):
  try:
    return pulse_DAL.add_pulse(pulse_dto)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

##########################################
# BP
##########################################
@app.get(f"{ROOT_PATH}/bpstats/{{user_id}}", response_model=List[BpDto], response_model_exclude_unset=False)
async def get_bp_by_user(user_id: int, current_user: User = Depends(get_current_active_user)):

  print("")
  print("")
  print("")
  print("get bp by user")
  print(user_id)
  print("")
  print("")
  print("")


  bp_stats = bp_DAL.get_bp_by_user(user_id)
  if bp_stats == None:
      raise HTTPException(status_code=404, detail="User not found")
  return bp_stats

@app.post(f'{ROOT_PATH}/bpstats/{{user_id}}/{{bp_id}}', status_code=201) #201 = created
async def update_bp(user_id: int, bp_id: int, bp_dto: BpDto, current_user: User = Depends(get_current_active_user)):
  try:
    bp_DAL.update_bp(bp_dto)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.delete(f'{ROOT_PATH}/bpstats/{{user_id}}/{{bp_id}}', status_code=201) #201 = created
async def delete_bp(user_id: int, bp_id: int, current_user: User = Depends(get_current_active_user)):
  try:
    bp_DAL.delete_bp(bp_id)
    return None
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.post(f'{ROOT_PATH}/bpstats/', status_code=201) #201 = created
async def create_bp(bp_dto: BpDto, current_user: User = Depends(get_current_active_user)):
  try:
    return bp_DAL.add_bp(bp_dto)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))