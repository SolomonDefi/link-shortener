# Solomon Link Shortener

API based URL shortener to generate and redirect links

## Install

Python 3.9+ is required.

[Poetry](https://python-poetry.org/docs/#installation) is used for dependency management.

```
poetry install
```

## Run

### Development

```
poetry run python application.py
```

### Production

```
TBD
```

## API Documentation

Routes marked *Authenticated* must provide an `access_token`

### Short URL Redirect
`GET /<string:short_link>`

Converts a short URL to a full one and returns a 301 redirect.
Query parameters are forwarded.

#### Responses
- `301`: Successful redirect
- `404`: Short link not found

### Get Short URL
`GET /api/links/<string:short_link>/`

Get information about a short URL.

#### Responses
- `200`: Success
```
"url": {
    "id": <integer>,
    "created": <datetime>,
    "short": <string>,
    "short_url": <url>,
    "target": <url>,
}
```
- `404` Short link not found

### Create Short URL
`POST /api/links/`\
*Authenticated*

Create a short URL. `short` and `fallback` are used if available, in that order.
If neither are available, an attempt is made to generate a unique random string of lowercase/capital/digits, starting with length 4.

#### JSON Parameters
Name          | Type    | Required | Note
------------- | ------- | -------- | ------------
access_token  | string  | Yes      | 
short         | string  | No       | Preferred short code
fallback      | string  | No       | Fallback short code
target        | string  | Yes      | The target for redirection
testing       | boolean | No       | Default=False, if True the short URL is not persisted

#### Responses
- `201`: Short link created
```
"url": {
    "id": <integer>,
    "created": <datetime>,
    "short": <string>,
    "short_url": <url>,
    "target": <url>,
}
```
- `401`: Invalid access token
- `400`: Invalid target, error generating short code
