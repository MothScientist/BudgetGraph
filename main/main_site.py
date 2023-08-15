from flask import Flask, render_template, request
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API token value from environment variable
token = os.getenv("BOT_TOKEN")
secret_key_users = os.getenv("SECRET_KEY_USERS_DB")
secret_key_families = os.getenv("SECRET_KEY_FAMILIES_DB")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route('/')
def index():
    return render_template("index.html", title="Budget control - Home page")


@app.route('/auth', methods=["GET", "POST"])  # send password in POST request
def auth():
    if request.method == "POST":
        print(request.form)  # request.args - GET, request.form - POST
    return render_template("auth.html", title="Budget control - Authorization")


@app.route('/household')
def household():
    return render_template("household.html", title="Budget control - Household")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", title="PAGE NOT FOUND")


if __name__ == "__main__":
    app.run(debug=True)  # change on False before upload on server
