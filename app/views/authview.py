from fastapi import APIRouter
from app.models.apimodels import UserSchema, UserLoginSchema, UserGetResponse, UserGetTokenResponse
from app.controller.apicontroller import ApiControllerUser

auth_router = APIRouter()


@auth_router.post('/register', response_model=UserGetResponse)
async def create_user(user: UserSchema):
    return await ApiControllerUser.create_user(user=user)


@auth_router.post('/token', response_model=UserGetTokenResponse)
async def generate_token(user: UserLoginSchema):
    return await ApiControllerUser.generate_token_user(user=user)
