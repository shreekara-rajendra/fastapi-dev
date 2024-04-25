from fastapi import Depends,status,HTTPException
from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings

# password flow Bearer type token...tokenurl means the url where the client can get the token
#  this checks the authorization header of the request packet and check if it is of format {Bearer <token>}
# the url is './token'
# this extracts the token and provides it
#also for this to work the tokenurl should use oauth2formdata
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
'''
we need to define the secret key,expiration time,algorithm
'''
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_jwt_token(data : dict):
    ##data is the payload.
    to_encode = data.copy()
    expiry_time = datetime.utcnow() + timedelta(minutes = float(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp':expiry_time})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return jwt_token

def verify_jwt_token(token : str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        userid:int = payload.get('user_id')
        print(userid)
        if userid is None :
            raise credentials_exception
        token_data = schemas.TokenData(id = userid)
    except JWTError:
        raise credentials_exception
    return token_data
    
## we can use the get_current _user as a dependency in the path operation that needs to be protected
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail =f"could not validate credentials"
                                          ,headers={"WWW-Authenticate" : "Bearer"})
    return verify_jwt_token(token,credentials_exception)
    
                    
    