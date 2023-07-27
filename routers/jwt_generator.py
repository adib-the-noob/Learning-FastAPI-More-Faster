from fastapi import Depends, HTTPException, status
from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta    

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "4e88f3a29cc0404fb1de73da89b8b68d0511866f18a4d7800aa8df224dda73ba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_access_token(username : str, user_id : int, expires_delta : timedelta):
    encode = {'sub' : username, 'id' : user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp' : expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-token")

def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
        return {'username' : username, 'id' : user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    
    