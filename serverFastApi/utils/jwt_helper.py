# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from typing import Optional
# from pydantic import BaseModel

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     email: str = None
#     disabled: Optional[bool] = None

# class Jwt_Helper:
    
#   #https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
#   jwt_config = {
#       "SECRET_KEY": "e41f43bcf9af08116d93df5d74f56cfd4b9a39584073a3bf44f216ce729c210a",
#       "ALGORITHM": "HS256",
#       "ACCESS_TOKEN_EXPIRE_MINUTES": 30
#   }

#   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#   @classmethod
#   def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):

#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, cls.jwt_config["SECRET_KEY"], algorithm = cls.jwt_config["ALGORITHM"])
#     return encoded_jwt

#   @classmethod
#   async def get_current_user(cls, token: str = Depends(cls.oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, cls.jwt_config["SECRET_KEY"], algorithms=[cls.jwt_config["ALGORITHM"]])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

#   @classmethod
#   async def get_current_active_user(cls, current_user: User = Depends(cls.get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user