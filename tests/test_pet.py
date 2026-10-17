import allure
import requests
from allure_commons.types import Severity
from base_request import base_request


PET_ID = 9001


@allure.feature("Pet")
@allure.story("Создание питомца")
@allure.severity(Severity.CRITICAL)
def test_create_pet():
    pet_data = {
        "id": PET_ID,
        "name": "TestPet",
        "status": "available"
    }

    response = base_request.post("pet", body=pet_data)

    assert response["id"] == PET_ID
    assert response["name"] == "TestPet"
    assert response["status"] == "available"


@allure.feature("Pet")
@allure.story("Получение питомца")
@allure.severity(Severity.NORMAL)
def test_get_pet():
    response = base_request.get("pet", PET_ID)

    assert response["id"] == PET_ID
    assert response["name"] == "TestPet"


@allure.feature("Pet")
@allure.story("Изменение питомца")
@allure.severity(Severity.CRITICAL)
def test_update_pet():
    pet_data = {
        "id": PET_ID,
        "name": "UpdatedPet",
        "status": "sold"
    }

    response = requests.put(
        "https://petstore.swagger.io/v2/pet",
        json=pet_data
    )

    assert response.status_code == 200

    result = response.json()
    assert result["id"] == PET_ID
    assert result["name"] == "UpdatedPet"
    assert result["status"] == "sold"


@allure.feature("Pet")
@allure.story("Удаление питомца")
@allure.severity(Severity.NORMAL)
def test_delete_pet():
    response = base_request.delete("pet", PET_ID)

    assert response["message"] == str(PET_ID)

@allure.feature("Pet")
@allure.story("Получение несуществующего питомца")
@allure.severity(Severity.NORMAL)
def test_get_nonexistent_pet():
    response = requests.get(
        "https://petstore.swagger.io/v2/pet/999999999"
    )

    assert response.status_code == 404


@allure.feature("Pet")
@allure.story("Создание питомца с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_pet_with_invalid_data():
    response = requests.post(
        "https://petstore.swagger.io/v2/pet",
        json={"id": "invalid", "name": 123}
    )

    assert response.status_code >= 400 or response.json().get("id") != "invalid"

@allure.feature("Pet")
@allure.story("Изменение питомца с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_update_pet_with_invalid_data():
    response = requests.put(
        "https://petstore.swagger.io/v2/pet",
        json={"id": "invalid", "name": 123}
    )

    assert response.status_code >= 400 or response.json().get("id") != "invalid"


@allure.feature("Pet")
@allure.story("Удаление несуществующего питомца")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_pet():
    response = requests.delete(
        "https://petstore.swagger.io/v2/pet/999999999"
    )

    assert response.status_code >= 400



