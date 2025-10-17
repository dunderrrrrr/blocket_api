# Preparations

## Tokens

Depending on which endpoints you want to use, you may need a token. Most of the endpoints does not require a token, but some do. See required parameters for each endpoint. 

How to get access to your token is described [here](https://github.com/dunderrrrrr/blocket_api?tab=readme-ov-file#-blocket-api-token).

The token can be passed as a query parameter (`token`) or as a header (`X-Token: <token>`). See the examples for more info.

## Making requests

Make the request with any http client, we strongly recommend using [httpx](https://www.python-httpx.org/) if working with Python. This API is rate limited to 5 requests/second, so keep yourself cool!