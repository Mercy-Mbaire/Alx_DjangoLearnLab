import requests
import random
import string
import time

BASE_URL = 'http://127.0.0.1:8000/api'

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_user():
    username = f'user_{get_random_string()}'
    password = 'testpassword123'
    email = f'{username}@example.com'
    url = f'{BASE_URL}/accounts/register/'
    data = {'username': username, 'email': email, 'password': password}
    response = requests.post(url, data=data)
    return response.json().get('token'), username, response.json().get('user')['id']

def test_follows_feed():
    print("Creating users...")
    token1, user1, id1 = create_user()
    token2, user2, id2 = create_user()
    
    headers1 = {'Authorization': f'Token {token1}'}
    headers2 = {'Authorization': f'Token {token2}'} # User 2 will contain the tests

    print(f"\nUser 1 ({user1}) creating a post...")
    post_data = {'title': 'User 1 Post', 'content': 'Content from User 1.'}
    response = requests.post(f'{BASE_URL}/posts/', headers=headers1, data=post_data)
    print(f"Create Post Status: {response.status_code}")

    print(f"\nUser 2 ({user2}) checking feed (Should be empty)...")
    response = requests.get(f'{BASE_URL}/feed/', headers=headers2)
    print(f"Feed Status: {response.status_code}")
    print(f"Feed Count: {len(response.json())}")

    print(f"\nUser 2 following User 1...")
    response = requests.post(f'{BASE_URL}/accounts/follow/{id1}/', headers=headers2)
    print(f"Follow Status: {response.status_code}")

    print(f"\nUser 2 checking feed (Should see User 1's post)...")
    response = requests.get(f'{BASE_URL}/feed/', headers=headers2)
    print(f"Feed Status: {response.status_code}")
    print(f"Feed Count: {len(response.json())}")
    if len(response.json()) > 0:
        print(f"Feed Item Title: {response.json()[0]['title']}")

    print(f"\nUser 2 unfollowing User 1...")
    response = requests.post(f'{BASE_URL}/accounts/unfollow/{id1}/', headers=headers2)
    print(f"Unfollow Status: {response.status_code}")

    print(f"\nUser 2 checking feed (Should be empty again)...")
    response = requests.get(f'{BASE_URL}/feed/', headers=headers2)
    print(f"Feed Status: {response.status_code}")
    print(f"Feed Count: {len(response.json())}")

if __name__ == '__main__':
    test_follows_feed()
