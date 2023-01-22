from app.models.apimodels import UserSchema, UserLoginSchema
from app.models.db import User, User_Pydantic
from passlib.hash import bcrypt
from config.config import CONFIG
import jwt
from typing import Union, Optional
from app.utils.hunter_co import verification_email
from app.utils.clearbit import get_clearbit_data
from app.exception.apiexception import api_exception


class UserDBController:
    @staticmethod
    async def authenticate_user(user: UserLoginSchema) -> Union[str, User]:
        user_obj = await User.get_or_none(email=user.email)
        if not user_obj:
            return "Email doesn't exist"
        if not user_obj.verify_password(user.password):
            return 'Wrong password'
        return user_obj

    @staticmethod
    async def create_user(user: UserSchema) -> User:
        if await verification_email(user.email) == 'invalid':
            raise api_exception(status_code=404, detail='Invalid email address')
        if await get_clearbit_data(user.email):
            """When executing, you can get additional information"""
            pass
        new_user = await User.create(email=user.email, password_hash=bcrypt.hash(user.password))
        await new_user.save()
        return new_user

    @staticmethod
    async def generate_token(user: User) -> str:
        user_obj = await User_Pydantic.from_tortoise_orm(user)
        return jwt.encode(user_obj.dict(), CONFIG.JWT_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM)

    @staticmethod
    async def get_user(pk: int) -> Optional[User]:
        return await User.get_or_none(pk=pk)
