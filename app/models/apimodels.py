from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserSchema(UserBase):
    class Config:
        schema_extra = {
            'example': {
                'email': 'user@example.com',
                'password': 'userpassword'
            }
        }


class UserLoginSchema(UserSchema):
    pass


class UserGetResponse(UserBase):
    id: int


class UserGetTokenResponse(BaseModel):
    access_token: str
    token_type: str


class PostText(BaseModel):
    text: str


class PostBase(PostText):
    id: int
    user_id: int


class PostEvaluation(BaseModel):
    like: int = 0
    dislike: int = 0


class PostGetResponse(PostBase, PostEvaluation):
    pass


class PostsGetResponse(BaseModel):
    posts: List[PostGetResponse]


class PostAddRequest(PostText):
    pass


class PostAddResponse(PostGetResponse):
    pass


class PostUpdateRequest(PostText):
    pass


class PostUpdateResponse(PostGetResponse):
    pass
