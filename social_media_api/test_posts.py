import requests
import random
import string

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
    return response.json().get('token'), username

def test_posts_comments():
    print("Creating users...")
    token1, user1 = create_user()
    token2, user2 = create_user()
    
    headers1 = {'Authorization': f'Token {token1}'}
    headers2 = {'Authorization': f'Token {token2}'}

    print(f"\nUser 1 ({user1}) creating a post...")
    post_data = {'title': 'First Post', 'content': 'This is the first post content.'}
    response = requests.post(f'{BASE_URL}/posts/', headers=headers1, data=post_data)
    print(f"Create Post Status: {response.status_code}")
    post_id = response.json().get('id')

    print(f"\nUser 2 ({user2}) commenting on User 1's post...")
    comment_data = {'post': post_id, 'content': 'Nice post!'}
    response = requests.post(f'{BASE_URL}/comments/', headers=headers2, data=comment_data)
    print(f"Create Comment Status: {response.status_code}")
    comment_id = response.json().get('id')

    print(f"\nUser 2 trying to delete User 1's post (Should Fail)...")
    response = requests.delete(f'{BASE_URL}/posts/{post_id}/', headers=headers2)
    print(f"Delete Post (Unauthorized) Status: {response.status_code}")

    print(f"\nUser 1 updating their post...")
    update_data = {'title': 'Updated Post Title', 'content': 'Updated content.'}
    response = requests.put(f'{BASE_URL}/posts/{post_id}/', headers=headers1, data=update_data)
    print(f"Update Post Status: {response.status_code}")

    print(f"\nFiltering posts by title...")
    response = requests.get(f'{BASE_URL}/posts/?search=Updated', headers=headers2)
    print(f"Filter Search Status: {response.status_code}")
    print(f"Search Results: {len(response.json())}") # Access count directly for pagination or list len

if __name__ == '__main__':
    test_posts_comments()
