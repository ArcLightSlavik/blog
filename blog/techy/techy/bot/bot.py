import httpx
import random
import configparser

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)


class Bot:
    def __init__(self, number_of_users, max_posts_per_user, max_likes_per_user, url):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.url = url

    def create_user(self):
        json_creds = {
            'username': fake.user_name(),
            'password': fake.password(length=12),
        }
        response = httpx.post(url=self.url + 'user', json=json_creds)
        response.raise_for_status()
        if response.status_code == 201:
            return json_creds
        return None

    def authenticate(self, auth_data):
        response = httpx.post(
            url=self.url + 'authenticate',
            json=auth_data
        )
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token

    def create_posts(self, auth_data):
        for _ in range(1, int(self.max_posts_per_user)):
            post_json = {
                'title': fake.city(),
                'text': fake.text()
            }
            token = self.authenticate(auth_data=auth_data)
            httpx.post(
                url=self.url + 'post',
                headers={'Authorization': f"Bearer {token}"},
                json=post_json
            ).raise_for_status()
        return 'OK'

    def create_likes(self, auth_data):
        token = self.authenticate(auth_data=auth_data)
        response = httpx.get(
            url=self.url + 'user/posts',
            headers={'Authorization': f"Bearer {token}"}
        )
        response.raise_for_status()
        posts = response.json()
        for _ in range(1, int(self.max_likes_per_user)):
            post = random.choice(posts)
            try:
                if random.randint(0, 9) % 2 == 0:
                    httpx.post(
                        url=self.url + 'post/like',
                        headers={'Authorization': f"Bearer {token}"},
                        json={'post_id': post['id']}
                    ).raise_for_status()
                else:
                    httpx.post(
                        url=self.url + 'post/dislike',
                        headers={'Authorization': f"Bearer {token}"},
                        json={'post_id': post['id']}
                    ).raise_for_status()
            except Exception as exception:
                # this happens if the post is already liked and is getting liked again
                # like -> dislike -> like | okay
                # like -> dislike -> dislike | not okay
                print(f'{exception} fired')


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('bot_config.ini')

    bot = Bot(**config['MAIN'])
    for _ in range(int(bot.number_of_users)):
        auth = bot.create_user()
        bot.create_posts(auth_data=auth)
        bot.create_likes(auth_data=auth)
