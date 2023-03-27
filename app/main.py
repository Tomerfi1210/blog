from fastapi import FastAPI, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.controller.blog_controller import BlogController
from app.controller.post_controller import PostController
from app.controller.like_controller import LikeController
from app.controller.comment_controller import CommentController
from app.schema.model import (
    SignUpSchema,
    PostSchema,
    PostInDBSchema,
    PostsSchema,
)
from pydantic import constr
from app.schema.auth_schema import Token
from app.auth.auth import (
    authenticate_user_decorator,
    create_access_token,
    get_current_active_user,
)
from app.tables import User
from datetime import timedelta
from typing import Annotated
from app.utills import get_access_token_expire_minutes

app = FastAPI()


@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_schema: SignUpSchema = Depends(SignUpSchema)):
    controller = BlogController()

    await controller.signup_user(signup_schema)

    return f"User {signup_schema.username} created"


@app.post("/token", response_model=Token, tags=[])
@authenticate_user_decorator
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    access_token_expires = timedelta(minutes=get_access_token_expire_minutes())
    access_token = await create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="Bearer")


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_schema: PostSchema = Depends(),
):
    controller = PostController()

    post_schem_db = PostInDBSchema(
        title=post_schema.title, content=post_schema.content, author_id=current_user.id
    )

    post_id = await controller.create_post(post_schem_db)

    return {"post_id": post_id}


@app.get("/all_posts", status_code=status.HTTP_200_OK, response_model=PostsSchema)
async def get_all_posts(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    controller = PostController()

    posts = await controller.get_all_posts()

    return PostsSchema(posts=posts)


@app.delete("/delete_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(
    current_user: Annotated[User, Depends(get_current_active_user)], post_id: int
):
    controller = PostController()

    await controller.delete_post(post_id, current_user.id)


@app.patch("/edit_post/{post_id}", status_code=status.HTTP_200_OK)
async def modify_post(
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_id: int,
    post_schema: PostSchema = Depends(),
):
    controller = PostController()

    post_id = await controller.edit_post(post_id, current_user.id, post_schema)

    return {"post_id": post_id}


@app.put("/like_post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def like_post(
    current_user: Annotated[User, Depends(get_current_active_user)], post_id: int
):
    controller = LikeController()

    await controller.like_post(post_id, current_user.id)


@app.delete("/delete_like/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    current_user: Annotated[User, Depends(get_current_active_user)], post_id: int
):
    controller = LikeController()

    await controller.delete_like(post_id, current_user.id)


@app.put("/comment/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def add_comment(
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_id: int,
    comment: constr(max_length=1000),
):
    controller = CommentController()

    await controller.add_comment(post_id, current_user.id, comment)


@app.delete(
    "/delete_comment/{post_id}/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_id: int,
    comment_id: int,
):
    controller = CommentController()

    await controller.delete_comment(comment_id, post_id, current_user.id)


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
