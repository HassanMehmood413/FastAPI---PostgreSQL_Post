from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import schema, database, models, oauth2
from datetime import datetime, timedelta, timezone
from .config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret key and algorithm settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credential_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')

        # Check if user_id exists and is numeric
        if user_id is None or not user_id.isdigit():
            raise credential_exception
        
        return schema.TokenData(id=int(user_id))
    except JWTError:
        raise credential_exception
    

def get_current_user(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    # Verify the token and retrieve user data
    token_data = verify_token(token, credentials_exception)
    
    # Fetch the user from the database using the token's user id
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    if user is None:
        raise credentials_exception
    
    return user  # Return the user object directly, not a Depends object
