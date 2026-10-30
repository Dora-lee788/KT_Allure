import allure
import requests
from base_request import base_request


URL = "https://petstore.swagger.io/v2"
PET_ID = 9001


def pet_data(name="TestPet", status="available"):
    return {
        "id": PET_ID,
        "name": name,
        "photoUrls": ["https://example.com/pet.jpg"],
        "status": status
    }


@allure.feature("Pet")
@allure.story("Создание питомца")
@allure.severity(Severity.CRITICAL)
def test_create_pet():
    response = base_request.post("pet", body=pet_data())

    assert response["id"] == PET_ID
    assert response["name"] == "TestPet"
    assert response["photoUrls"] == ["https://example.com/pet.jpg"]


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
    data = pet_data("UpdatedPet", "sold")

    response = requests.put(f"{URL}/pet", json=data)

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
    response = requests.get(f"{URL}/pet/999999999")

    assert response.status_code == 404


@allure.feature("Pet")
@allure.story("Создание питомца с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_pet_with_invalid_data():
    response = requests.post(
        f"{URL}/pet",
        json={"id": "invalid", "name": 123}
    )

    assert response.status_code in (400, 405)


@allure.feature("Pet")
@allure.story("Изменение питомца с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_update_pet_with_invalid_data():
    response = requests.put(
        f"{URL}/pet",
        json={"id": "invalid", "name": 123, "photoUrls": []}
    )

    assert response.status_code == 400


@allure.feature("Pet")
@allure.story("Удаление несуществующего питомца")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_pet():
    response = requests.delete(f"{URL}/pet/999999999")

    assert response.status_code == 404


@allure.feature("Pet")
@allure.story("Поиск питомцев по статусу")
@allure.severity(Severity.NORMAL)
def test_find_pets_by_status():
    response = requests.get(
        f"{URL}/pet/findByStatus",
        params={"status": "available"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(pet["status"] == "available" for pet in response.json())


@allure.feature("Pet")
@allure.story("Поиск питомцев по некорректному статусу")
@allure.severity(Severity.NORMAL)
def test_find_pets_by_invalid_status():
    response = requests.get(
        f"{URL}/pet/findByStatus",
        params={"status": "invalid_status"}
    )

    assert response.status_code == 400


@allure.feature("Pet")
@allure.story("Поиск питомцев по тегам")
@allure.severity(Severity.NORMAL)
def test_find_pets_by_tags():
    response = requests.get(
        f"{URL}/pet/findByTags",
        params={"tags": "1"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@allure.feature("Pet")
@allure.story("Поиск питомцев по несуществующему тегу")
@allure.severity(Severity.NORMAL)
def test_find_pets_by_nonexistent_tag():
    response = requests.get(
        f"{URL}/pet/findByTags",
        params={"tags": "999999999"}
    )

    assert response.status_code == 200
    assert response.json() == []


@allure.feature("Pet")
@allure.story("Изменение питомца через форму")
@allure.severity(Severity.CRITICAL)
def test_update_pet_with_form():
    pet_id = 9002

    create = requests.post(
        f"{URL}/pet",
        json={
            "id": pet_id,
            "name": "FormPet",
            "photoUrls": ["https://example.com/pet.jpg"],
            "status": "available"
        }
    )

    assert create.status_code == 200

    response = requests.post(
        f"{URL}/pet/{pet_id}",
        data={"name": "FormPetUpdated", "status": "sold"}
    )

    assert response.status_code == 200

    updated = requests.get(f"{URL}/pet/{pet_id}").json()

    assert updated["name"] == "FormPetUpdated"
    assert updated["status"] == "sold"


@allure.feature("Pet")
@allure.story("Изменение через форму несуществующего питомца")
@allure.severity(Severity.NORMAL)
def test_update_nonexistent_pet_with_form():
    response = requests.post(
        f"{URL}/pet/999999999",
        data={"name": "MissingPet", "status": "sold"}
    )

    assert response.status_code in (404, 405)
