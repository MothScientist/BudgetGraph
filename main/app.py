from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
import os
import re
import datetime
from dotenv import load_dotenv
from database_control import get_db, close_db, create_table_group, FDataBase
from validators.registration import registration_validator, token_validator
from validators.login import login_validator
from password_hashing import getting_hash, get_salt


load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config.from_object(__name__)

# Get the secret key to encrypt the Flask session from an environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config.update(dict(DATABASE=os.path.join(app.root_path, "db.sqlite3")))

app.teardown_appcontext(close_db)  # Disconnects the database connection after a query

app.permanent_session_lifetime = datetime.timedelta(days=14)  # session lifetime in browser cookies


@app.route('/')
def homepage():
    return render_template("homepage.html", title="Budget control - Home page")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        username = request.form["username"]
        psw = request.form["password"]
        tg_link = request.form["tg_link"]
        token = request.form["token"]

        # If the token field is empty
        if len(request.form['token']) == 0:  # user creates a new group
            if registration_validator(username, psw, tg_link):

                dbase = FDataBase(get_db())

                if user_token := dbase.create_group(tg_link):

                    group_id = token_validator(user_token)
                    psw_salt = get_salt()
                    create_table_group(f"budget_{group_id}")

                    if dbase.add_user_to_db(username, psw_salt, getting_hash(psw, psw_salt), group_id, tg_link):
                        flash("Registration completed successfully!", category="success")
                        flash(f"{username}, your token: {user_token}", category="success_token")

        # User is added to an existing group
        if len(token) == 32:
            if registration_validator(username, psw, tg_link):
                if group_id := token_validator(token):  # new variable "group_id" (int)

                    dbase = FDataBase(get_db())
                    psw_salt = get_salt()

                    if dbase.add_user_to_db(username, psw_salt, getting_hash(psw, psw_salt), group_id, tg_link):

                        # redirecting the user to a personal account (he already has a group token)
                        session["userLogged"] = username
                        return redirect(url_for("household", username=session["userLogged"], token="token"))

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
    session.permanent = True

    if "userLogged" in session:  # If the client has logged in before
        return redirect(url_for("household", username=session["userLogged"]))

    # here the POST request is checked and the presence of the user in the database is checked
    if request.method == "POST":
        username = request.form["username"]
        psw = request.form["password"]
        token = request.form["token"]
        dbase = FDataBase(get_db())
        psw_salt = dbase.get_salt_by_username(username)

        if psw_salt and login_validator(username, getting_hash(psw, psw_salt), token):

            session["userLogged"] = username
            dbase.update_user_last_login(username)
            return redirect(url_for("household", username=session["userLogged"]))

        else:
            flash("Error. Please try again and if the problem persists, contact technical support.", category="error")
        # request.args - GET, request.form - POST

    return render_template("login.html", title="Budget control - Login")


@app.route('/household/<username>', methods=["GET", "POST"])  # user's personal account
def household(username):
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)

    dbase = FDataBase(get_db())
    token = dbase.get_token_by_username(username)
    table_name = f"budget_{dbase.get_group_id_by_token(token)}"

    if request.method == "POST":

        if "submit_button_1" in request.form:  # Processing the "Add to table" button for form 1
            income = request.form.get("income")
            income = re.sub(r"[^0-9]", "", income)

            if not re.match(r"^(?!0\d)\d{0,14}$", income):
                flash("Error", category="error")

            description_1 = request.form.get("description_1")

            if dbase.add_monetary_transaction_to_db(table_name, username, int(income), description_1):
                flash("Data added successfully.", category="success")
            else:
                flash("Error adding data to database.", category="error")

            print(f"Income: {income},\nDescription: {description_1}")

        elif "submit_button_2" in request.form:  # Processing the "Add to table" button for form 2
            expense = request.form.get("expense")
            expense = re.sub(r"[^0-9]", "", expense)

            if not re.match(r"^(?!0\d)\d{0,14}$", expense):
                flash("Error", category="error")

            description_2 = request.form.get("description_2")

            if dbase.add_monetary_transaction_to_db(table_name, username, int(expense)*(-1), description_2):
                flash("Data added successfully.", category="success")
            else:
                flash("Error adding data to database.", category="error")

            print(f"Expense: {expense},\nDescription: {description_2}")

    headers = ["№", "Total", "Username", "Transfer", "DateTime", "Description"]
    data = dbase.select_data_for_household_table(table_name)

    return render_template("household.html", title=f"Budget control - {username}",
                           token=token, username=username, data=data, headers=headers)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop("userLogged", None)  # removing the "userLogged" key from the session (browser cookies)
    return redirect(url_for('homepage'))  # redirecting the user to another page, such as the homepage


@app.errorhandler(401)
def page_not_found(error):
    return render_template("error401.html", title="UNAUTHORIZED"), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", title="PAGE NOT FOUND"), 404


if __name__ == "__main__":
    app.run(debug=True)  # change on False before upload on server
