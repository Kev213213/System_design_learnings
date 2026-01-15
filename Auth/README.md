# Authentication & Authorization


## Keycloak setup

In a nutshell, 
- Flask redirect to keycloak server for auth
- user authenticates on Keycloak 
- Flask receives a ID+auth token from keycloak
- flask creates a session token if user succeeds


```
+--------+        +-------------+        +------------------+
|  User  |        |  Flask App  |        |   Keycloak       |
|Browser |        | (Authlib)   |        | (OIDC Server)    |
+--------+        +-------------+        +------------------+
     |                    |                         |
     |  GET /login        |                         |
     |------------------->|                         |
     |                    |                         |
     |                    |  Create state + nonce   |
     |                    |  Store in Flask session |
     |                    |                         |
     |                    | 302 Redirect             |
     |                    |------------------------>|
     |                    |   /authorize             |
     |                    |   + client_id            |
     |                    |   + redirect_uri         |
     |                    |   + scope                |
     |                    |   + state                |
     |                    |   + nonce                |
     |                    |                         |
     |  Redirect           |                         |
     |------------------->|                         |
     |                    |                         |
     |   Login form        |                         |
     |<-------------------|                         |
     |                    |                         |
     |  Enter credentials |                         |
     |------------------------------->|              |
     |                                | Authenticate  |
     |                                | Create KC     |
     |                                | Session       |
     |                                |               |
     |                                | 302 Redirect  |
     |                                |-------------->|
     |                                |  /callback    |
     |                                |  ?code=XXX    |
     |                                |  &state=YYY  |
     |                    |                         |
     |  Redirect           |                         |
     |------------------->|                         |
     |                    |                         |
     |                    | Validate state (CSRF)   |
     |                    | Exchange code for token |
     |                    |------------------------>|
     |                    |  POST /token             |
     |                    |  + client_secret         |
     |                    |                         |
     |                    |   ID Token               |
     |                    |   Access Token           |
     |                    |<------------------------|
     |                    |                         |
     |                    | Create Flask session    |
     |                    | Store user info         |
     |                    |                         |
     |   Logged in page    |                         |
     |<-------------------|                         |
     |                    |                         |

```

## Concepts involved

* **Keycloak terms** : realm > clients 
                             > users

* Keycloak sends token (ID token + auth token) | auth token is based on client roles & realm roles conjuntion too.


* **Cross Site Request Forgery (CSRF)**
    - user logs in a server, which generates & store cookie info in the browser
    - attacker leads the user to his own site , this site has script to read the cookie n send request on users behalf without his consent.

## To explore 

- [ ] How postgres integrates with Keycloak
- [ ] Use Keycloak with authentication features
- [ ] How CSRF can be prevented ?
- [ ] Build a full fledge app using fastapi on AWS.
