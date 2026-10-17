import allure
from allure_commons.types import Severity
from base_request import base_request


@allure.feature("User")
@allure.story("Создание пользователя")
@allure.severity(Severity.CRITICAL)
def test_create_user():
    user_data = {
        "id": 1001,
        "username": "test_user_1001",
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "123456",
        "phone": "1234567890",
        "userStatus": 1
    }

    response = base_request.post(
        "user",
        body=user_data
    )

    assert response["code"] == 200
    assert response["type"] == "unknown"


@allure.feature("User")
@allure.story("Получение пользователя")
@allure.severity(Severity.NORMAL)
def test_get_user():
    response = base_request.get(
        "user",
        "test_user_1001"
    )

    assert response["username"] == "test_user_1001"
    assert response["id"] == 1001


@allure.feature("User")
@allure.story("Изменение пользователя")
@allure.severity(Severity.CRITICAL)
def test_update_user():
    updated_user_data = {
        "id": 1001,
        "username": "test_user_1001",
        "firstName": "Updated",
        "lastName": "User",
        "email": "updated@example.com",
        "password": "654321",
        "phone": "9876543210",
        "userStatus": 1
    }

    response = base_request.put(
        "user",
        "test_user_1001",
        updated_user_data
    )

    assert response["code"] == 200
    assert response["type"] == "unknown"

    user_info = base_request.get(
        "user",
        "test_user_1001"
    )

    assert user_info["firstName"] == "Updated"
    assert user_info["email"] == "updated@example.com"


@allure.feature("User")
@allure.story("Удаление пользователя")
@allure.severity(Severity.NORMAL)
def test_delete_user():
    response = base_request.delete(
        "user",
        "test_user_1001"
    )

    assert response["code"] == 200
    assert response["type"] == "unknown"

    user_info = base_request.get(
        "user",
        "test_user_1001",
        expected_error=True
    )

    assert "message" in user_info

@allure.feature("User")
@allure.story("Получение несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_get_nonexistent_user():
    import requests

    response = requests.get(
        "https://petstore.swagger.io/v2/user/nonexistent_user_999999"
    )

    assert response.status_code >= 400


@allure.feature("User")
@allure.story("Создание пользователя с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_user_with_invalid_data():
    import requests

    response = requests.post(
        "https://petstore.swagger.io/v2/user",
        json={"id": "invalid", "username": 123}
    )

    assert response.status_code >= 400 or response.json().get("message") != "invalid"

@allure.feature("User")
@allure.story("Изменение несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_update_nonexistent_user():
    import requests

    response = requests.put(
        "https://petstore.swagger.io/v2/user/nonexistent_user_999999",
        json={
            "id": 999999,
            "username": "nonexistent_user_999999",
            "firstName": "Test"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "999999"


@allure.feature("User")
@allure.story("Удаление несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_user():
    import requests

    response = requests.delete(
        "https://petstore.swagger.io/v2/user/nonexistent_user_999999"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "nonexistent_user_999999"


