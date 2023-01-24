import pytest
from app.models.db import User, Post
from app.controller.dbcontroller import EvaluationDBController


@pytest.mark.anyio
async def test_registrate_user(client):
    response = await client.post('/auth/register', json={
        'email': 'iteszero@tes.by',
        'password': 'itestpassword'
    })

    test_user = await User.get(pk=1)

    assert response.status_code == 200
    assert test_user.pk == 1
    assert test_user.email == 'iteszero@tes.by'
    assert test_user.verify_password(password='itestpassword')


@pytest.mark.anyio
async def test_generate_user_token(client, user):
    response = await client.post('/auth/token', json={
        'email': user.email,
        'password': 'itestpassword'
    })

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


@pytest.mark.anyio
@pytest.mark.parametrize('url', ('/auth/register',  '/auth/token', ))
async def test_auth_exception(client, url):
    response = await client.post(url)

    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.anyio
async def test_get_posts(client, user_headers):
    response = await client.get('/api/v1/pd/post/', headers=user_headers)

    assert response.status_code == 200
    assert len(response.json()['posts']) == 0


@pytest.mark.anyio
async def test_add_post(client, user_headers):
    response = await client.post('/api/v1/pd/post/', headers=user_headers, json={"text": "string"})

    assert response.status_code == 200
    assert response.json() == {'dislike': 0, 'id': 1, 'like': 0, 'text': 'string', 'user_id': 2}


@pytest.mark.anyio
async def test_get_post(client, user_headers, post):
    response = await client.get(f'/api/v1/pd/post/{post.id}', headers=user_headers)

    assert response.status_code == 200
    assert response.json()['text'] == 'ConfTest'


@pytest.mark.anyio
async def test_update_post(client, user_headers, post):
    response = await client.put(f'/api/v1/pd/post/{post.id}',
                                headers=user_headers,
                                json={'text': 'UpdateTest'})

    assert response.status_code == 200
    assert response.json()['text'] == 'UpdateTest'


@pytest.mark.anyio
async def test_delete_post(client, user_headers, post):
    response = await client.delete(f'/api/v1/pd/post/{post.id}', headers=user_headers)

    check_post = await Post.get_or_none(pk=post.id)

    assert response.status_code == 200
    assert not check_post


@pytest.mark.anyio
@pytest.mark.parametrize('evaluation', ('like', 'dislike'))
async def test_like_or_dislike_my_post(client, user_headers, post, evaluation):
    response = await client.get(f'/api/v1/pd/post/{post.id}/{evaluation}', headers=user_headers)

    assert response.status_code == 404
    assert response.json() == {'detail': "The author can't like/dislike his posts"}


@pytest.mark.anyio
async def test_like_post(client, user_headers, another_post):
    response = await client.get(f'/api/v1/pd/post/{another_post.id}/like', headers=user_headers)

    post_like = await EvaluationDBController.get_count_post_evaluation(post_id=another_post.id, evaluation=True)

    assert response.status_code == 200
    assert post_like == 1


@pytest.mark.anyio
async def test_dislike_post(client, user_headers, another_post):
    response = await client.get(f'/api/v1/pd/post/{another_post.id}/dislike', headers=user_headers)

    post_dislike = await EvaluationDBController.get_count_post_evaluation(post_id=another_post.id, evaluation=False)

    assert response.status_code == 200
    assert post_dislike == 1


@pytest.mark.anyio
async def test_get_posts_exception(client):
    response = await client.get('/api/v1/pd/post/')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.anyio
async def test_add_post_exception(client):
    response = await client.post('/api/v1/pd/post/')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.anyio
async def test_get_post_exception(client, post):
    response = await client.get(f'/api/v1/pd/post/{post.id}')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.anyio
async def test_update_post_exception(client, post):
    response = await client.put(f'/api/v1/pd/post/{post.id}')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.anyio
async def test_delete_post_exception(client, post):
    response = await client.delete(f'/api/v1/pd/post/{post.id}')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.anyio
@pytest.mark.parametrize('evaluation', ('like', 'dislike'))
async def test_like_or_dislike_post_exception(client, another_post, evaluation):
    response = await client.get(f'/api/v1/pd/post/{another_post.id}/{evaluation}')

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}