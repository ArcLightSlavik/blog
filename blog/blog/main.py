from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from .postgres import TortoiseSettings

from .exceptions import LikeException
from .exceptions import CredentialsException

from .api.user_api import user_router
from .api.post_api import post_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)


@app.on_event("startup")
def startup():
    config = TortoiseSettings.generate()
    register_tortoise(
        app,
        db_url=config.db_url,
        generate_schemas=config.generate_schemas,
        modules=config.modules,
    )


@app.exception_handler(CredentialsException)
def credentials_exception_handler(_request: Request, _exc: CredentialsException):
    return JSONResponse(
        status_code=401,
        content="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(LikeException)
def like_exception_handler(_request: Request, _exc: LikeException):
    return JSONResponse(
        status_code=400,
        content="You can't like/dislike a post that has already been liked/disliked"
    )
