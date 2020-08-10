import requests
from faker import Faker
from faker.providers import internet
import json
import random

fake = Faker()
fake.add_provider(internet)


class Bot:
    def __init__(self, number_of_users, max_posts_per_user, max_likes_per_user, url):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.url = url

    def create_user(self):
        data = {'username': fake.user_name(),
                'password': fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True),
                'email': fake.email()}
        response = requests.post(url=self.url + 'users/', data=data)
        if response.status_code == 201:
            login_response = requests.post(url=self.url + 'login', data={'username': data.get('username'),
                                                                         'password': data.get('password')})
            auth_data = json.loads(login_response.content)
            return auth_data
        return None

    def jwt_verify(self, auth_data):
        jwt_access = auth_data.get('access')
        jwt_refresh = auth_data.get('refresh')
        jwt_verification = requests.post(url=self.url + 'login/verify',
                                         headers={'Authorization': f"JWT {jwt_access}"},
                                         data={'token': jwt_access})
        if jwt_verification.status_code != 200:
            response = requests.post(url=self.url + 'login/refresh',
                                     headers={'Authorization': f"JWT {jwt_refresh}"})
            auth_data = json.loads(response.content)
            jwt_access = auth_data.get('access')
            jwt_refresh = auth_data.get('refresh')
        return jwt_access, jwt_refresh

    def create_posts(self, auth_data):
        post_counter = 0
        for _ in range(random.randint(1, int(self.max_posts_per_user))):
            post_data = {
                'title': fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                'body': fake.text(max_nb_chars=250, ext_word_list=None)
            }
            jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
            response = requests.post(url=self.url + 'api/posts',
                                     headers={'Authorization': f"JWT {jwt_access}"},
                                     data=post_data)
            if response.status_code == 201:
                post_counter += 1
        return post_counter

    def create_likes(self, auth_data):
        jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
        response = requests.get(url=self.url + 'api/posts',
                                headers={'Authorization': f"JWT {jwt_access}"})
        posts = json.loads(response.text)
        actions = 0
        while actions < random.randint(1, int(self.max_likes_per_user)):
            slug = posts[random.randint(0, len(posts) - 1)].get('slug')
            response = requests.post(url=self.url + f'api/posts/{slug}/like',
                                     headers={'Authorization': f"JWT {jwt_access}"})
            if response.status_code == 401:
                jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
                requests.post(url=self.url + f'api/posts/{slug}/like',
                              headers={'Authorization': f"JWT {jwt_access}"})
            actions += 1
        return actions
