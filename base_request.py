
import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        if request_type == 'GET':
            response = requests.get(url)
        elif request_type == 'POST':
            response = requests.post(url, json=data)
        elif request_type == 'PUT':
            response = requests.put(url, json=data)
        else:
            response = requests.delete(url)

        print(f'{request_type} request')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        pprint.pprint(response.text)

        try:
            pprint.pprint(response.json())
        except ValueError:
            pass

        pprint.pprint('***********')

        return response

    def get(self, endpoint, endpoint_id=None, expected_error=False):
        if endpoint_id is not None:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        else:
            url = f'{self.base_url}/{endpoint}'

        response = self._request(
            url,
            'GET',
            expected_error=expected_error
        )

        return response.json()

    def post(self, endpoint, endpoint_id=None, body=None):
        if endpoint_id is not None:
            url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        else:
            url = f'{self.base_url}/{endpoint}'

        response = self._request(
            url,
            'POST',
            data=body
        )

        return response.json()

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'

        response = self._request(
            url,
            'PUT',
            data=body
        )

        return response.json()

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'

        response = self._request(
            url,
            'DELETE'
        )

        return response.json()


BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'

base_request = BaseRequest(BASE_URL_PETSTORE)
