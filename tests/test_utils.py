import pytest
from app.utils.hunter_сo import verification_email
from app.utils.clearbit import get_clearbit_data


@pytest.mark.anyio
async def test_hunter_co(user):
    result = await verification_email(user.email)

    assert result == 'accept_all'


@pytest.mark.anyio
@pytest.mark.xfail(raisez=KeyError)
async def test_hunter_co_exception(user):
    await verification_email(user.id)


@pytest.mark.anyio
async def test_clearbit(user):
    result = await get_clearbit_data(user.email)

    assert result


@pytest.mark.anyio
@pytest.mark.skip
async def test_clearbit_exception(user):
    await get_clearbit_data('None')
