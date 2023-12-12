from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.pydantic_models import PostURL, User, UserInDB, Token, TokenData
from app.service.database import add_custom_url_to_db, add_random_url_to_db, create_new_user, get_all_urls, get_one_url

# Temporary return messages
SUCCESS_MESSAGE = "Process successful!"
ERROR_MESSAGE = "Sorry, we could not process your request."

router = APIRouter(prefix="/api", tags=["url_actions"])
auth_router = APIRouter(prefix="/users", tags=["user_actions"])

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@auth_router.post("/create_user")
async def create_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    existing_user = get_user(fake_users_db, username)
    if existing_user:
        return {"temp_message": "This username already exists"}

    hashed_password = get_password_hash(form_data.password)

    response = create_new_user(username, hashed_password)

    if response["status_code"] == 200:
        response["message"] = f"User '{username}' created successfully."
    else:
        response["message"] = f"Error occurred, user '{username}' not created."

    return response


# -----------------------------------------------------------------------------------

@router.post("/shorten_url")
async def shorten_url(record: Annotated[PostURL, Body(title="Pydantic Model for URL")]):
    if record.custom_url:
        # Custom url provided, attempt to add custom url to DB
        response = add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        response = add_random_url_to_db(original_url=record.original_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response


@router.get("/list_urls")
async def list_urls():
    response = get_all_urls()

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response


@router.get("/redirect/{short_url}")
async def redirect(short_url: Annotated[str, 'short_url to be used for redirection'] = None):
    if not short_url:
        return {"status_code": 400, "payload": "Bad Input"}

    # Check DB for short_url key
    response = get_one_url(short_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
        url_item = response["payload"]
        if url_item and type(url_item) != str:
            url_to_go_to = url_item.original_url
            return RedirectResponse(url=url_to_go_to, status_code=303)

    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response
