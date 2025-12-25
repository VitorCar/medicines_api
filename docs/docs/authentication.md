# Autenticação

A Medicines API utiliza **JWT**.

## Endpoints
- POST api/authentication/token/
- POST api/authentication/token/refresh/
- POST api/authentication/token/verify/

## Header padrão
```http
Authorization: Bearer <token>
