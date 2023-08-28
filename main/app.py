from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
import os
from dotenv import load_dotenv
from database_control import get_db, close_db, FDataBase
from token_generation import get_token
from validators.registration import registration_validator, token_validator
from validators.login import login_validator
from password_hashing import generate_hash


# Load environment variables from .env file
load_dotenv()

# TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
app.config.from_object(__name__)

# Get the secret key to encrypt the Flask session from an environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config.update(dict(DATABASE=os.path.join(app.root_path, "db.sqlite3")))

app.teardown_appcontext(close_db)  # Disconnects the database connection after a query


@app.route('/')
def homepage():
    return render_template("homepage.html", title="Budget control - Home page")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        # If the token field is empty
        if len(request.form['token']) == 0:  # user creates a new group
            if registration_validator(
                    request.form["username"], request.form["password"], request.form["tg_link"]
            ):
                user_token = get_token()
                flash("Registration completed successfully!", category="success")
                flash(f"{request.form['username']}, "
                      f"your token: {user_token}", category="success_token")
                print(request.form)
            else:
                pass  # the flash function is called inside the validator

        # User is added to an existing group
        if len(request.form["token"]) == 32:
            if (registration_validator(
                        request.form["username"], request.form["password"], request.form["tg_link"]) and
                    token_validator(request.form["token"])):
                flash("Registration completed successfully!", category="success")
            else:
                pass  # the flash function is called inside the validator

        # User made a mistake when entering the token
        if len(request.form["token"]) > 0 and len(request.form["token"]) != 32:
            flash("Error - token length must be 32 characters", category="error")

    return render_template("registration.html", title="Budget control - Registration")


@app.route('/login', methods=["GET", "POST"])  # send password in POST request
def login():
    if "userLogged" in session:  # If the client has logged in before
        return redirect(url_for("household", username=session["userLogged"]))

    # here the POST request is checked and the presence of the user in the database is checked
    if request.method == "POST":
        if login_validator(request.form["username"], generate_hash(request.form["password"]), request.form["token"]):
            session["userLogged"] = request.form["username"]
            return redirect(url_for("household", username=session["userLogged"]))
        else:
            pass
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
