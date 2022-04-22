import requests


def create_api_token(username, password):
    """Response
    {
        "access_token": "NgCXRK...MzYjw",
        "refresh_token": "NgAagA...Um_SHo"
    }
    """
    response = requests.request(
     method="post",
     url='http://127.0.0.1:8000/' + 'api/token/',
     data={
         "username": username,
         "password": password
     }
    ).json()

    return response
