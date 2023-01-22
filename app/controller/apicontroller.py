from app.controller.dbcontroller import PostDBController, EvaluationDBController
from app.controller.userdbcontroller import UserDBController
from app.models.apimodels import PostGetResponse, PostsGetResponse, PostAddResponse, PostUpdateResponse, \
    UserGetResponse, UserGetTokenResponse
from fastapi import status
from app.exception.apiexception import api_exception
from app.models.db import Post, User


class ApiControllerPost:

    @staticmethod
    async def get_post_evaluation(post: Post):
        like = await EvaluationDBController.get_count_post_evaluation(post_id=post.id, evaluation=True)
        dislike = await EvaluationDBController.get_count_post_evaluation(post_id=post.id, evaluation=False)
        return like, dislike

    @staticmethod
    async def get_all_posts() -> PostsGetResponse:
        posts_list = await PostDBController.get_all_posts()
        return PostsGetResponse(
            posts=[
                PostGetResponse(
                    id=el.id,
                    text=el.text,
                    user_id=el.user_id,
                    like=(await ApiControllerPost.get_post_evaluation(post=el))[0],
                    dislike=(await ApiControllerPost.get_post_evaluation(post=el))[1],
                ) for el in posts_list
            ]
        )

    @staticmethod
    async def get_post(pk: int) -> PostGetResponse:
        post = await PostDBController.get_post(pk=pk)
        if post:
            like_post, dislike_post = await ApiControllerPost.get_post_evaluation(post=post)
            return PostGetResponse(**post.__dict__, like=like_post, dislike=dislike_post)
        else:
            raise api_exception(status_code=404, detail='Post not found')

    @staticmethod
    async def add_post(text: str, user_id: int) -> PostAddResponse:
        post = await PostDBController.add_post(text=text, user_id=user_id)
        return PostAddResponse(**post.__dict__)

    @staticmethod
    async def edit_post(pk: int, text: str, user_id: int) -> PostUpdateResponse:
        post = await PostDBController.edit_post(pk=pk, text=text, user_id=user_id)
        if post:
            like_post, dislike_post = await ApiControllerPost.get_post_evaluation(post=post)
            return PostUpdateResponse(**post.__dict__, like=like_post, dislike=dislike_post)
        else:
            raise api_exception(status_code=404, detail='Post not found')

    @staticmethod
    async def delete_post(pk: int, user_id: int) -> int:
        post = await PostDBController.delete_post(pk=pk, user_id=user_id)
        if post:
            return status.HTTP_200_OK
        else:
            raise api_exception(status_code=404, detail='Post not found')

    @staticmethod
    async def add_post_evaluation(post_id: int, user_id: int, evaluation: bool) -> int:
        post = await PostDBController.add_post_evaluation(post_id=post_id, user_id=user_id, evaluation=evaluation)
        if post:
            return status.HTTP_200_OK
        else:
            raise api_exception(status_code=404, detail='Post not found')


class ApiControllerUser:

    @staticmethod
    async def create_user(user) -> UserGetResponse:
        if await User.get_or_none(email=user.email):
            raise api_exception(status_code=401, detail='User already registered')
        new_user = await UserDBController.create_user(user=user)
        return UserGetResponse(id=new_user.id, email=new_user.email, password=new_user.password_hash)

    @staticmethod
    async def generate_token_user(user) -> UserGetTokenResponse:
        check = await UserDBController.authenticate_user(user=user)
        if isinstance(check, str):
            raise api_exception(status_code=401, detail=check)
        token = await UserDBController.generate_token(user=check)
        return UserGetTokenResponse(access_token=token, token_type='bearer')
