# edx-manager-access-api

Expose API to add grant user staff and superuser privileges

## Usage

### Base Url

`${STUDIO_URL}/sn-api`

### Grant user privileges

`POST /manager-access/grant_access`

The JSON body requires one parameters.

-   `email`: An existing user.

Sample request

```json
{
    "email": "admin@example.com"
}
```

### Revoke user privileges

`POST /manager-access/revoke_access`

The JSON body requires one parameters.

-   `email`: An existing user.

Sample request

```json
{
    "email": "admin@example.com"
}
```
