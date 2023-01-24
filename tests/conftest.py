import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from app import app
from app.controller.userdbcontroller import UserDBController
from app.controller.dbcontroller import PostDBController
from app.models.apimodels import UserSchema

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ['app.models.db', 'aerich.models']}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
async def user(client):
    return await UserDBController.create_user(UserSchema(
        email='ites@tes.by', password='itestpassword'))


@pytest.fixture
async def generate_token(user):
    return await UserDBController.generate_token(user)


@pytest.fixture
def user_headers(generate_token) -> dict:
    return {'Authorization': f'Bearer {generate_token}'}


@pytest.fixture
async def post(user):
    return await PostDBController.add_post(text='ConfTest', user_id=user.id)


@pytest.fixture(scope="session")
async def another_user(client):
    return await UserDBController.create_user(UserSchema(
        email='itestwo@tes.by', password='itestpassword'))


@pytest.fixture
async def another_post(another_user):
    return await PostDBController.add_post(text='ConfTest', user_id=another_user.id)
