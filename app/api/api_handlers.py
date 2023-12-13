from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.pydantic_models import PostURL, User, Token, TokenData
import app.service.database as service


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


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
    user = service.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def is_admin_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = service.authenticate_user(form_data.username, form_data.password)
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


@auth_router.get("/me/", response_model=User)
async def show_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@auth_router.post("/create_user")
async def create_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    existing_user = service.get_user(username)
    if existing_user:
        return {"temp_message": "This username already exists"}

    response = service.create_new_user(username, form_data.password)

    if response["status_code"] == 200:
        response["payload"] = f"User '{username}' created successfully."
    else:
        response["payload"] = f"Error occurred, user '{username}' not created."

    return response


@auth_router.post("/change_password/")
async def change_password(
    old_password: Annotated[str, "User's previous password"],
    new_password: Annotated[str, "User's new password"],
    current_user: Annotated[User, Depends(get_current_user)]
):

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = service.change_password(old_password, new_password, current_user)

    return response


@auth_router.get("/list_all_users")
async def list_all_users(is_admin: Annotated[bool, Depends(is_admin_user)]):
    if is_admin:
        response = service.get_all_pynamodb_users()
        return response


@auth_router.post("/update_url_limit")
async def update_url_limit(
        username: Annotated[str, "username of user to change url limit for"],
        new_limit: Annotated[int, "new url limit"],
        is_admin: Annotated[bool, Depends(is_admin_user)]
):

    if not is_admin:
        response = service.update_user_url_limit(username, new_limit)
        return response






# -----------------------------------------------------------------------------------

@router.post("/shorten_url")
async def shorten_url(record: Annotated[PostURL, Body(title="Pydantic Model for URL")]):
    if record.custom_url:
        # Custom url provided, attempt to add custom url to DB
        response = service.add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        response = service.add_random_url_to_db(original_url=record.original_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response


@router.get("/list_urls")
async def list_urls():
    response = service.get_all_urls()

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
    response = service.get_one_url(short_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
        url_item = response["payload"]
        if url_item and type(url_item) != str:
            url_to_go_to = url_item.original_url
            return RedirectResponse(url=url_to_go_to, status_code=303)

    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response
