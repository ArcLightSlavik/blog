from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from .v1.database import engine

from .v1.exceptions import LikeException
from .v1.exceptions import CredentialsException

from .v1.api.user_api import user_router
from .v1.api.post_api import post_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)

from .v1.models.user_model import User
from .v1.models.post_model import Post
from .v1.models.like_model import Like

User.metadata.create_all(engine)
Post.metadata.create_all(engine)
Like.metadata.create_all(engine)


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
