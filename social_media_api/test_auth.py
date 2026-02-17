import requests
import random
import string

BASE_URL = 'http://127.0.0.1:8000/api/accounts'

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

USERNAME = f'user_{get_random_string()}'
PASSWORD = 'testpassword123'
EMAIL = f'{USERNAME}@example.com'

def test_registration():
    url = f'{BASE_URL}/register/'
    data = {
        'username': USERNAME,
        'email': EMAIL,
        'password': PASSWORD,
        'bio': 'Test bio'
    }
    response = requests.post(url, data=data)
    print(f'Registration Status: {response.status_code}')
    print(f'Registration Response: {response.json()}')
    return response.json().get('token')

def test_login():
    url = f'{BASE_URL}/login/'
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(url, data=data)
    print(f'Login Status: {response.status_code}')
    print(f'Login Response: {response.json()}')
    return response.json().get('token')

def test_profile(token):
    url = f'{BASE_URL}/profile/'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url, headers=headers)
    print(f'Profile Status: {response.status_code}')
    print(f'Profile Response: {response.json()}')

if __name__ == '__main__':
    print(f"Testing with User: {USERNAME}")
    print("Testing Registration...")
    token = test_registration()
    if token:
        print("\nSkipping separate login test as we have token, but testing login endpoint anyway...")
        
    print("\nTesting Login...")
    login_token = test_login()
    if login_token:
        print(f"\nTesting Profile with token: {login_token}")
        test_profile(login_token)
