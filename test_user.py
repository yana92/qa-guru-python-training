import pytest
import requests

from pytest import mark

# base_url = "https://reqres.in"
base_url = "http://0.0.0.0:8000"


@pytest.mark.parametrize("user_id, expected_email", [
    (2, "janet.weaver@reqres.in"),
])
def test_get_user(user_id, expected_email):
    """Test успешного запроса /api/users/{user_id}"""
    url = f"{base_url}/api/users/{user_id}"

    response = requests.get(url)
    result = response.json()

    assert response.status_code == 200, 'Неожиданный код ответа'
    assert "data" in result, "В ответе отсутсвует объект data"
    data = result["data"]
    assert data["id"] == user_id, f"Ожидался id {user_id}, вернулся: {data['id']}"
    assert data["email"] == expected_email, \
        f"Ожидаемый email: {expected_email}, вернулся {data['email']}"
    assert "support" in result, "В ответе не вернулся объект support"


@mark.parametrize('user_id', [3])
def test_get_user_not_found(user_id):
    """Тест неуспешного запроса /api/users/{user_id}. Пользователь не найден."""
    url = f"{base_url}/api/users/{user_id}"
    response = requests.get(url)
    assert response.status_code == 404, 'Неожиданный код ответа'
    assert response.json() == {}, f'В ответе вернулся не пустой объект: {response.json()}'


@mark.parametrize('name, job', [('morpheus', 'leader')])
def test_post_user(name, job):
    """Успешное создание пользователя"""
    url = f"{base_url}/api/users"

    json = {
        'name': name,
        'job': job
    }
    response = requests.post(url, json=json)
    assert response.status_code == 201, 'Неожиданный код ответа'
    assert response.json()['name'] == name, 'Значение поля name в ответе отличается от ожидаемого'
    assert response.json()['job'] == job, 'Значение поля job в ответе отличается от ожидаемого'
    assert 'id' in response.json(), 'В ответе не вернулось поле id'
    assert 'createdAt' in response.json(), 'В ответе не вернулось поле createdAt'


@mark.parametrize('email, password', [('eve.holt@reqres.in', 'pistol')])
def test_login(email, password):
    """Успешная авторизация пользователя"""
    url = f"{base_url}/api/login"
    json = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=json)
    assert response.status_code == 200, 'Неожиданный код ответа'
    assert 'token' in response.json(), 'В ответе не вернулся token'
    assert response.json()['token'] != '', 'В ответе вернулся пустой token'


@mark.parametrize('email', ["eve.holt@reqres.in"])
def test_login_missing_password(email):
    """Запрос авторизации без обязательного параметра password"""
    url = f"{base_url}/api/login"
    json = {
        "email": email
    }
    response = requests.post(url, json=json)
    assert response.status_code == 400, 'Неожиданный код ответа'
    assert response.json()["error"] == "Missing password", 'Текст ошибки отличается от ожидаемого'


@pytest.mark.parametrize('user_id, payload', [
    ('2', {'name': 'Morpheus', 'job': 'zion resident'}),
])
def test_patch_user(user_id, payload):
    """Успешное обновление юзера методом PATCH /api/users/{user_id}"""
    url = f'{base_url}/api/users/{user_id}'
    response = requests.patch(url, json=payload)
    assert response.status_code == 200, 'Неожиданный код ответа'
    data = response.json()
    assert data['name'] == payload.get('name'), 'name в ответе не соответствует ожидаемому'
    assert data['job'] == payload.get('job'), 'job в ответе не соответсвует ожидаемому'
    assert 'updatedAt' in data, 'В ответе не вернулось поле updatedAt'


@mark.parametrize('payload', [
    {'name': 'Morpheus', 'job': 'Leader'},
    {}
])
@mark.parametrize('user_id', [0])
def test_patch_user_not_found(user_id, payload):
    """Обновление несуществующего пользователя"""
    url = f'{base_url}/api/users/{user_id}'
    response = requests.patch(url, json=payload)
    assert response.status_code == 404, 'Неожиданный код ответа'


@mark.parametrize('user_id', [2])
def test_delete_user(user_id):
    """Успешное удаление пользователя"""
    url = f"{base_url}/api/users/{user_id}"
    response = requests.delete(url)
    assert response.status_code == 204, 'Неожиданный код ответа'
