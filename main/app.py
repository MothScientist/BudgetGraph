from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
import os
from dotenv import load_dotenv
from database_control import get_db, close_db, FDataBase
from validators.registration import registration_validator, token_validator
from validators.login import login_validator
from password_hashing import generate_hash


load_dotenv()  # Load environment variables from .env file

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
                dbase = FDataBase(get_db())
                if user_token := dbase.create_group(request.form["tg_link"]):
                    group_id = token_validator(user_token)
                    if dbase.add_user_to_db(request.form["username"], generate_hash(request.form["password"]),
                                            group_id, request.form["tg_link"]):
                        flash("Registration completed successfully!", category="success")
                        flash(f"{request.form['username']}, "
                              f"your token: {user_token}", category="success_token")

        # User is added to an existing group
        if len(request.form["token"]) == 32:
            if registration_validator(request.form["username"], request.form["password"], request.form["tg_link"]):
                if group_id := token_validator(request.form["token"]):  # new variable "group_id" (int)
                    dbase = FDataBase(get_db())
                    if dbase.add_user_to_db(request.form["username"], generate_hash(request.form["password"]),
                                            group_id, request.form["tg_link"]):
                        # redirecting the user to a personal account (he already has a group token)
                        session["userLogged"] = request.form["username"]
                        return redirect(url_for("household", username=session["userLogged"]))
                    else:
                        flash("Error creating user. Please try again and if the problem persists, "
                              "contact technical support.", category="error")
                else:
                    flash("There is no group with this token, please check the correctness of the entered data!",
                          category="error")

        # User made a mistake when entering the token
        if len(request.form["token"]) > 0 and len(request.form["token"]) != 32:
            flash("Error - token length must be 32 characters", category="error")

    return render_template("registration.html", title="Budget control - Registration")


@app.route('/login', methods=["GET", "POST"])  # send password in POST request and in hash
def login():
    if "userLogged" in session:  # If the client has logged in before
        return redirect(url_for("household", username=session["userLogged"]))

    # here the POST request is checked and the presence of the user in the database is checked
    if request.method == "POST":
        if login_validator(request.form["username"], generate_hash(request.form["password"]), request.form["token"]):
            session["userLogged"] = request.form["username"]
            dbase = FDataBase(get_db())
            dbase.update_user_last_login(request.form["username"])
            return redirect(url_for("household", username=session["userLogged"]))
        else:
            flash("Error. Please try again and if the problem persists, contact technical support.", category="error")
        # request.args - GET, request.form - POST

    return render_template("login.html", title="Budget control - Login")


@app.route('/household/<username>')  # user's personal account
def household(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)
    return render_template("household.html", title=f"Budget control - {username}")


# @app.route('/logout', methods=['GET'])
# def logout():
#     # Removing the "userLogged" key from the session
#     session.pop("userLogged", None)
#
#     # Redirecting the user to another page, such as the homepage
#     return redirect(url_for('homepage'))


@app.errorhandler(401)
def page_not_found(error):
    return render_template("error401.html", title="UNAUTHORIZED"), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", title="PAGE NOT FOUND"), 404


if __name__ == "__main__":
    app.run(debug=True)  # change on False before upload on server
