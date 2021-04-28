import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, jsonify, send_from_directory
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import json
from flask_cors import CORS, cross_origin
 

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config.from_object(app_config)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY']='abcdefg'
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/setToken")
@cross_origin()
def setToken():
    if not session.get("user"):
       print("IN setToken, no user sesssion found ")
       return redirect(url_for("login"))
    session["token"]='I am your token J'
    print('token = ' + session.get("token"))
    return jsonify( 
         token=f'{session.get("token")}' 
         )
    
@app.route("/getToken")
@cross_origin()
def getToken():
    if not session.get("user"):
       return redirect(url_for("login"))
    print('getToken = ' + session.get("token"))
    return jsonify( 
         token=f'{session.get("token")} ' 
         )

@app.route("/login")
def login():
    print ("Entering login")
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        print("Entering " + app_config.REDIRECT_PATH)
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        print("passing " + app_config.REDIRECT_PATH)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        # Vincent added below:
        print ('***************** : ' + json.dumps(result.get("id_token_claims")))
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
        return render_template("auth_error.html", result={"error" : "Value Error", "error_description":"Not signed in yet !!"})
    return redirect(url_for("entry"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/entry")
def entry():
    if not session.get("user"):
       return redirect(url_for("login"))
    return send_from_directory(app.static_folder,'index.html')

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
 app.run(host='127.0.0.1', port=5000, debug=True)
    

