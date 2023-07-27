from jose import JWTError, jwt
from datetime import datetime, timedelta    

SECRET_KEY = "4e88f3a29cc0404fb1de73da89b8b68d0511866f18a4d7800aa8df224dda73ba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_access_token(username : str, user_id : int, expires_delta : timedelta):
    encode = {'sub' : username, 'id' : user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp' : expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


