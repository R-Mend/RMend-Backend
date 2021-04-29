# Authentication

> Node Report Manager requires users to be authentication to access some routes

## Create a user

Creates a new user with a username and password. Anyone can call this route, however, if they use an email already connected to a current user it will fail.

`POST` /sign-up

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| email       | string | body | users email in the format of email@example.com |
| password    | string | body | secure password that will be encrypted |
| username    | string | body | users identification `First Last` format recommended |

## Login a user

Grants access to routes that require an authenticated user to use. Any signed-in user can access this route. Saves a `jwt token` to verify users' identity until it expires or the user logs out.

`GET` /login

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| email       | string | body | users email in the format of email@example.com |
| password    | string | body | secure password that will be encrypted |
| username    | string | body | users identification |

## Logout a user

Disconnects the current user by deactivating the jwt token. Any signed-in user can access this route.

`GET` /logout

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| none        |        |      |              |
