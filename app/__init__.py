from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.tortoise_config import AERICH_CONFIG
from app.controller.jwt_bearer import JWTBearer
from app.views.authview import auth_router
from app.views.apiview import router
from fastapi import Depends

app = FastAPI()

app.include_router(router=router, prefix='/api/v1/pd/post', dependencies=[Depends(JWTBearer())], tags=['API'])
app.include_router(router=auth_router, prefix='/auth', tags=['Authorize'])

register_tortoise(app, config=AERICH_CONFIG)
