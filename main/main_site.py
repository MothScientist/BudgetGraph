from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from database_control import get_db, close_db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from environment variable
TOKEN = os.getenv("BOT_TOKEN")
DATABASE = "db.sqlite3"
DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config.from_object(__name__)

# Get the secret key to encrypt the Flask session from an environment variable
app.config["SECRET_KEY"] = SECRET_KEY

app.config.update(dict(DATABASE=os.path.join(app.root_path, "db.sqlite3")))

app.teardown_appcontext(close_db)  # Disconnects the database connection after a query


@app.route('/')
def homepage():
    return render_template("homepage.html", title="Budget control - Home page")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        print(request.form)
    return render_template("registration.html", title="Budget control - Registration")


@app.route('/login', methods=["GET", "POST"])  # send password in POST request
def login():
    if "userLogged" in session:  # If the client has logged in before
        return redirect(url_for("household", username=session["userLogged"]))

    # here the POST request is checked and the presence of the user in the database is checked
    if request.method == "POST" and request.form.get("username") == "username":  # OK
        session["userLogged"] = request.form["username"]
        return redirect(url_for("household", username=session["userLogged"]))
        # print(request.form)  # request.args - GET, request.form - POST

    return render_template("login.html", title="Budget control - Login")


@app.route('/household/<username>')  # user's personal account
def household(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    return render_template("household.html", title=f"Budget control - {username}")


@app.errorhandler(401)
def page_not_found(error):
    return render_template("error401.html", title="UNAUTHORIZED"), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", title="PAGE NOT FOUND"), 404


if __name__ == "__main__":
    app.run(debug=True)  # change on False before upload on server
