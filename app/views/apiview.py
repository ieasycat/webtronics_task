from fastapi import APIRouter, Depends
from app.controller.jwt_bearer import get_current_user
from app.models.apimodels import PostGetResponse, PostsGetResponse, PostAddResponse, PostAddRequest, \
    PostUpdateResponse, PostUpdateRequest
from app.controller.apicontroller import ApiControllerPost

router = APIRouter()


@router.get('/', response_model=PostsGetResponse)
async def get_posts():
    """Get all posts"""
    return await ApiControllerPost.get_all_posts()


@router.get('/{pk:int}', response_model=PostGetResponse)
async def get_post(pk: int):
    """Get a post"""
    return await ApiControllerPost.get_post(pk=pk)


@router.put('/{pk:int}', response_model=PostUpdateResponse)
async def update_post(pk: int, text: PostUpdateRequest, current_user: int = Depends(get_current_user)):
    """Modifies a specific post from the current user"""
    return await ApiControllerPost.update_post(pk=pk, text=text.text, user_id=current_user)


@router.post('/', response_model=PostAddResponse)
async def add_post(text: PostAddRequest, current_user: int = Depends(get_current_user)):
    """Creates a new post for the current user"""
    return await ApiControllerPost.add_post(text=text.text, user_id=current_user)


@router.delete('/{pk:int}')
async def delete_post(pk: int, current_user: int = Depends(get_current_user)):
    """Delete a specific post from the current user"""
    return await ApiControllerPost.delete_post(pk=pk, user_id=current_user)


@router.get('/{pk:int}/like')
async def like_post(pk: int, current_user: int = Depends(get_current_user)):
    """Puts a like on a certain post"""
    return await ApiControllerPost.add_post_evaluation(post_id=pk, user_id=current_user, evaluation=True)


@router.get('/{pk:int}/dislike')
async def dislike_post(pk: int, current_user: int = Depends(get_current_user)):
    """Puts a dislike on a certain post"""
    return await ApiControllerPost.add_post_evaluation(post_id=pk, user_id=current_user, evaluation=False)
