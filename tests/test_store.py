import allure
from allure_commons.types import Severity
from base_request import base_request


@allure.feature("Store")
@allure.story("Получение инвентаря")
@allure.severity(Severity.NORMAL)
def test_get_inventory():
    response = base_request.get("store/inventory")

    assert isinstance(response, dict)
    assert len(response) > 0


@allure.feature("Store")
@allure.story("Создание заказа")
@allure.severity(Severity.CRITICAL)
def test_create_order():
    order_data = {
        "id": 5,
        "petId": 1,
        "quantity": 1,
        "shipDate": "2026-10-02T13:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    response = base_request.post(
        "store/order",
        body=order_data
    )

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

    response = base_request.get(
        "store/order",
        5,
        expected_error=True
    )

    assert "message" in response

@allure.feature("Store")
@allure.story("Получение несуществующего заказа")
@allure.severity(Severity.NORMAL)
def test_get_nonexistent_order():
    import requests

    response = requests.get(
        "https://petstore.swagger.io/v2/store/order/999999999"
    )

    assert response.status_code >= 400


@allure.feature("Store")
@allure.story("Создание заказа с некорректными данными")
@allure.severity(Severity.NORMAL)
def test_create_order_with_invalid_data():
    import requests

    response = requests.post(
        "https://petstore.swagger.io/v2/store/order",
        json={"id": "invalid", "petId": "invalid", "quantity": -1}
    )

    assert response.status_code >= 400 or response.json().get("id") != "invalid"

@allure.feature("Store")
@allure.story("Получение заказа с некорректным ID")
@allure.severity(Severity.NORMAL)
def test_get_order_with_invalid_id():
    import requests

    response = requests.get(
        "https://petstore.swagger.io/v2/store/order/invalid"
    )

    assert response.status_code >= 400


@allure.feature("Store")
@allure.story("Удаление несуществующего заказа")
@allure.severity(Severity.NORMAL)
def test_delete_nonexistent_order():
    import requests

    response = requests.delete(
        "https://petstore.swagger.io/v2/store/order/999999999"
    )

    assert response.status_code >= 400


