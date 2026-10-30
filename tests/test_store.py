import allure
import requests
from base_request import base_request


URL = "https://petstore.swagger.io/v2"


@allure.feature("Store")
@allure.story("Получение инвентаря")
@allure.severity(Severity.NORMAL)
def test_get_inventory():
    response = base_request.get("store/inventory")

    assert isinstance(response, dict)
    assert all(isinstance(value, int) for value in response.values())


@allure.feature("Store")
@allure.story("Создание заказа")
@allure.severity(Severity.CRITICAL)
def test_create_order():
    order_data = {
        "id": 5,
        "petId": 1,
        "quantity": 1,
        "shipDate": "2026-10-30T13:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    response = base_request.post("store/order", body=order_data)

    assert response["id"] == 5
    assert response["petId"] == 1
    assert response["quantity"] == 1
    assert response["status"] == "placed"


@allure.feature("Store")
@allure.story("Получение заказа")
@allure.severity(Severity.NORMAL)
def test_get_order():
    response = base_request.get("store/order", 5)

    assert response["id"] == 5
    assert response["status"] == "placed"


@allure.feature("Store")
@allure.story("Удаление заказа")
@allure.severity(Severity.NORMAL)
def test_delete_order():
    base_request.delete("store/order", 5)

    response = requests.get(f"{URL}/store/order/5")

    assert response.status_code == 404


@allure.feature("Store")
@allure.story("Получение несуществующего заказа")
@allure.severity(Severity.NORMAL)
def test_get_nonexistent_order():
    response = requests.get(f"{URL}/store/order/999999999")

    assert response.status_code in (400, 404)


@allure.feature("Store")
@allure.story("Создание заказа с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_order_with_invalid_data():
    response = requests.post(
        f"{URL}/store/order",
        json={
            "id": "invalid",
            "petId": "invalid",
            "quantity": -1
        }
    )

    assert response.status_code == 400


@allure.feature("Store")
@allure.story("Получение заказа с некорректным ID")
@allure.severity(Severity.NORMAL)
def test_get_order_with_invalid_id():
    response = requests.get(f"{URL}/store/order/invalid")

    assert response.status_code == 400


@allure.feature("Store")
@allure.story("Удаление несуществующего заказа")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_order():
    response = requests.delete(f"{URL}/store/order/999999999")

    assert response.status_code == 404


