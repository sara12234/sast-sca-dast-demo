import os
import subprocess

from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape

app = Flask(__name__)

# Secret lu depuis une variable d'environnement
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("La variable d'environnement SECRET_KEY est requise")

# Activation de la protection CSRF
csrf = CSRFProtect(app)

# Liste blanche des commandes autorisées
ALLOWED_COMMANDS = {
    "ls": ["ls", "-l"],
    "date": ["date"],
    "whoami": ["whoami"],
}


@app.route("/")
def index():
    return """
    <h1>Welcome to our Flask App</h1>
    <ul>
        <li><a href="/hello?name=World">Hello Page</a></li>
        <li><a href="/execute?cmd=ls">Execute Command Page</a></li>
        <li><a href="/admin">Admin Area</a></li>
    </ul>
    """


@app.route("/hello")
def hello():
    name = escape(request.args.get("name", "Guest"))

    return f"""
    <h1>Hello Page</h1>
    <p>Hello, {name}!</p>
    <p><a href="/">Back to Homepage</a></p>
    """


@app.route("/execute", methods=["GET"])
def execute():
    key = request.args.get("cmd", "ls")

    if key not in ALLOWED_COMMANDS:
        return "Commande non autorisée", 400

    result = subprocess.run(
        ALLOWED_COMMANDS[key],
        capture_output=True,
        text=True,
        check=False,
    )

    return f"""
    <h1>Execute Command Page</h1>
    <p>Executing command: <code>{escape(key)}</code></p>
    <pre>{escape(result.stdout)}</pre>
    <pre style="color: red;">{escape(result.stderr)}</pre>
    <p><a href="/">Back to Homepage</a></p>
    """


@app.route("/admin")
def admin():
    return """
    <h1>Admin Area</h1>
    <p>Accès réservé.</p>
    <p><a href="/">Back to Homepage</a></p>
    """
