import allure
import requests
from allure_commons.types import Severity
from base_request import base_request


URL = "https://petstore.swagger.io/v2"


def create_test_user(username="test_user_1001", user_id=1001):
    data = {
        "id": user_id,
        "username": username,
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "123456",
        "phone": "1234567890",
        "userStatus": 1
    }

    response = requests.post(f"{URL}/user", json=data)
    assert response.status_code == 200


@allure.feature("User")
@allure.story("Создание пользователя")
@allure.severity(Severity.CRITICAL)
def test_create_user():
    data = {
        "id": 1001,
        "username": "test_user_1001",
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "123456",
        "phone": "1234567890",
        "userStatus": 1
    }

    response = base_request.post("user", body=data)

    assert response["code"] == 200


@allure.feature("User")
@allure.story("Получение пользователя")
@allure.severity(Severity.NORMAL)
def test_get_user():
    create_test_user()

    response = base_request.get("user", "test_user_1001")

    assert response["username"] == "test_user_1001"
    assert response["id"] == 1001


@allure.feature("User")
@allure.story("Изменение пользователя")
@allure.severity(Severity.CRITICAL)
def test_update_user():
    create_test_user()

    data = {
        "id": 1001,
        "username": "test_user_1001",
        "firstName": "Updated",
        "lastName": "User",
        "email": "updated@example.com",
        "password": "654321",
        "phone": "9876543210",
        "userStatus": 1
    }

    response = base_request.put("user", "test_user_1001", data)

    assert response["code"] == 200

    user = base_request.get("user", "test_user_1001")

    assert user["firstName"] == "Updated"
    assert user["email"] == "updated@example.com"


@allure.feature("User")
@allure.story("Удаление пользователя")
@allure.severity(Severity.NORMAL)
def test_delete_user():
    create_test_user()

    response = base_request.delete("user", "test_user_1001")

    assert response["code"] == 200

    result = requests.get(f"{URL}/user/test_user_1001")

    assert result.status_code == 404


@allure.feature("User")
@allure.story("Получение несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_get_nonexistent_user():
    response = requests.get(
        f"{URL}/user/nonexistent_user_999999"
    )

    assert response.status_code == 404


@allure.feature("User")
@allure.story("Создание пользователя с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_user_with_invalid_data():
    response = requests.post(
        f"{URL}/user",
        json={"id": "invalid", "username": 123}
    )

    assert response.status_code == 400


@allure.feature("User")
@allure.story("Изменение несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_update_nonexistent_user():
    response = requests.put(
        f"{URL}/user/nonexistent_user_999999",
        json={
            "id": 999999,
            "username": "nonexistent_user_999999",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "123456",
            "phone": "1234567890",
            "userStatus": 1
        }
    )

    assert response.status_code == 404


@allure.feature("User")
@allure.story("Удаление несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_user():
    response = requests.delete(
        f"{URL}/user/nonexistent_user_999999"
    )

    assert response.status_code == 404


@allure.feature("User")
@allure.story("Создание пользователей массивом")
@allure.severity(Severity.CRITICAL)
def test_create_users_with_array():
    users = [
        {
            "id": 1101,
            "username": "array_user_1101",
            "firstName": "Array",
            "lastName": "User",
            "email": "array1101@example.com",
            "password": "123456",
            "phone": "1234567890",
            "userStatus": 1
        }
    ]

    response = requests.post(
        f"{URL}/user/createWithArray",
        json=users
    )

    assert response.status_code == 200

    user = requests.get(f"{URL}/user/array_user_1101")

    assert user.status_code == 200
    assert user.json()["id"] == 1101


@allure.feature("User")
@allure.story("Создание пользователей массивом с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_users_with_invalid_array():
    response = requests.post(
        f"{URL}/user/createWithArray",
        json={"username": 123}
    )

    assert response.status_code == 400


@allure.feature("User")
@allure.story("Создание пользователей списком")
@allure.severity(Severity.CRITICAL)
def test_create_users_with_list():
    users = [
        {
            "id": 1102,
            "username": "list_user_1102",
            "firstName": "List",
            "lastName": "User",
            "email": "list1102@example.com",
            "password": "123456",
            "phone": "1234567890",
            "userStatus": 1
        }
    ]

    response = requests.post(
        f"{URL}/user/createWithList",
        json=users
    )

    assert response.status_code == 200

    user = requests.get(f"{URL}/user/list_user_1102")

    assert user.status_code == 200
    assert user.json()["id"] == 1102


@allure.feature("User")
@allure.story("Создание пользователей списком с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_users_with_invalid_list():
    response = requests.post(
        f"{URL}/user/createWithList",
        json={"username": 123}
    )

    assert response.status_code == 400


@allure.feature("User")
@allure.story("Вход пользователя")
@allure.severity(Severity.NORMAL)
def test_login_user():
    create_test_user("login_user_1200", 1200)

    response = requests.get(
        f"{URL}/user/login",
        params={
            "username": "login_user_1200",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert response.text != ""


@allure.feature("User")
@allure.story("Вход с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_login_user_with_invalid_credentials():
    response = requests.get(
        f"{URL}/user/login",
        params={
            "username": "missing_user_999999",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 400


@allure.feature("User")
@allure.story("Выход пользователя")
@allure.severity(Severity.NORMAL)
def test_logout_user():
    response = requests.get(f"{URL}/user/logout")

    assert response.status_code == 200


@allure.feature("User")
@allure.story("Выход с использованием некорректного метода")
@allure.severity(Severity.NORMAL)
def test_logout_user_with_invalid_method():
    response = requests.post(f"{URL}/user/logout")

    assert response.status_code == 405


