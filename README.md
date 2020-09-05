# Blog

## Installation

### Option 1: Docker

Preffered over the other option

```bash
$ git clone https://github.com/ArcLightSlavik/blog.git
$ cd blog
$ docker-compose build
$ docker-compose up
```

### Option 2: Running directly

```bash
$ git clone https://github.com/ArcLightSlavik/blog.git
$ cd blog
$ pip3 install virtualenv
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ cd blog
$ cd techy
$ pip3 install -r requirements.txt
$ gunicorn -b :8000 -k uvicorn.workers.UvicornWorker --reload techy.main:app
```

## Usage

### Option 1: Postman 
```
Postman: https://www.getpostman.com/collections/5aa33f7c6239ea525429
```

### Option 2: List of endpoints
#### User
##### Create new user
```
URI: http://127.0.0.1:8000/user
Type: POST
Body: {
    "username": "username",
    "password": "password"
}
```
##### Auth
```
URI: http://127.0.0.1:8000/authenticate
Type: POST
Body: {
    "username": "username",
    "password": "password"
}
```

##### Get user info
```
URI: http://127.0.0.1:8000/user/info
Type: GET
Authorization: {
  Bearer Token: token_created_when_auth
}
```

##### Get user last login and last request
```
URI: http://127.0.0.1:8000/user/analytics
Type: GET
Authorization: {
  Bearer Token: token_created_when_auth
}
```

##### Get all the posts the user created
```
URI: http://127.0.0.1:8000/user/posts
Type: GET
Authorization: {
  Bearer Token: created_token
}
```

#### Post
##### Create a post
```
URI: http://127.0.0.1:8000/post
Type: POST
Authorization: {
  Bearer Token: token_created_when_auth
}
Body: {
  "title": "string",
  "text": "string"
}
```

##### Like a post
```
URI: http://127.0.0.1:8000/post/like
Type: POST
Authorization: {
  Bearer Token: token_created_when_auth
}
Body: {
    "post_id": 1
}
```

##### Dislike a post
```
URI: http://127.0.0.1:8000/post/dislike
Type: POST
Authorization: {
  Bearer Token: token_created_when_auth
}
Body: {
    "post_id": 1
}
```

##### Get number of likes and dislikes user did during a certain period of time (unix)
```
URI: http://127.0.0.1:8000/post/analytics/0/5000000000
Type: GET
Authorization: {
  Bearer Token: token_created_when_auth
}
```
