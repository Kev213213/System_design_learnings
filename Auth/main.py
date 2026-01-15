from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

oauth = OAuth(app)


keycloak = oauth.register(
    name="keycloak",
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=(
        f"{os.getenv('KEYCLOAK_BASE_URL')}"
        f"/realms/{os.getenv('KEYCLOAK_REALM')}"
        f"/.well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid profile email",
        "token_endpoint_auth_method": "client_secret_post"},
)

@app.route("/")
def home():
    if "user" in session:
        return f"Hello {session['user']['preferred_username']}!"
    return '<a href="/login">Login</a>'

@app.route("/test")
def test():
    print("==============================")
    print (os.getenv('KEYCLOAK_BASE_URL'))
    return 'testing'

@app.route("/login")
def login():
    # if "user" in session:
    #     return redirect("/")
    session.clear()
    return keycloak.authorize_redirect(
        redirect_uri="http://localhost:5000/callback"
    )

@app.route("/callback")
def callback():
    print("SESSION BEFORE TOKEN:", session)
    token = keycloak.authorize_access_token()
    print("TOKEN:", token)
    session["user"] = token["userinfo"]
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"{os.getenv('KEYCLOAK_BASE_URL')}/realms/{os.getenv('KEYCLOAK_REALM')}/protocol/openid-connect/logout"
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
