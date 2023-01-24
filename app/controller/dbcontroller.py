from app.models.db import Post, Evaluation
from typing import Optional
from tortoise.expressions import Q
from app.exception.apiexception import api_exception


class PostDBController:

    @staticmethod
    async def get_all_posts() -> list:
        return await Post.all()

    @staticmethod
    async def get_post(pk: int) -> Optional[Post]:
        return await Post.get_or_none(pk=pk)

    @staticmethod
    async def add_post(text: str, user_id: int) -> Post:
        return await Post.create(text=text, user_id=user_id)

    @staticmethod
    async def update_post(pk: int, user_id: int, text: str) -> Optional[Post]:
        post = await Post.get_or_none(pk=pk, user_id=user_id)
        if post:
            post.text = text
            await post.save()
            return post

    @staticmethod
    async def delete_post(pk: int, user_id: int) -> bool:
        post = await Post.get_or_none(pk=pk, user_id=user_id)
        if post:
            await post.delete()
            return True
        else:
            return False

    @staticmethod
    async def add_post_evaluation(post_id: int, user_id: int, evaluation: bool) -> bool:
        if not await Post.filter(Q(Q(pk=post_id), Q(user_id=user_id), join_type='AND')):
            return await EvaluationDBController.add_post_evaluation(
                post_id=post_id, user_id=user_id, evaluation=evaluation)
        else:
            raise api_exception(status_code=404, detail="The author can't like/dislike his posts")


class EvaluationDBController:

    @staticmethod
    async def add_post_evaluation(post_id: int, user_id: int, evaluation: bool) -> bool:
        post = await Evaluation.get_or_none(post_id=post_id, user_id=user_id)
        if post:
            post.evaluation = evaluation
            await post.save()
            return True
        else:
            await Evaluation.create(post_id=post_id, user_id=user_id, evaluation=evaluation)
            return True

    @staticmethod
    async def get_count_post_evaluation(post_id: int, evaluation: bool) -> int:
        return len(await Evaluation.filter(Q(Q(post_id=post_id), Q(evaluation=evaluation), join_type='AND')))
