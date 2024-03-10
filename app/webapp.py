from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
import os
from datetime import timedelta
from dotenv import load_dotenv
import asyncio
import sys

sys.path.append('../')

from app.db_manager import connect_db_flask_g, close_db_flask_g, create_table_group, DatabaseQueries  # noqa
from app.encryption import getting_hash, get_salt  # noqa
from app.validation import value_validation, description_validation, date_validation, registration_validation  # noqa
from app.logger import setup_logger  # noqa

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config.from_object(__name__)

# Get the secret key to encrypt the Flask session from an environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.teardown_appcontext(close_db_flask_g)  # Disconnects the database connection after a query

# session lifetime in browser cookies
app.permanent_session_lifetime = timedelta(days=14)  # timedelta from datetime module

logger_app = setup_logger("logs/AppLog.log", "app_loger")


@app.route('/')
def homepage():
    return render_template("homepage.html", title="Budget Graph - Homepage")


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username: str = request.form["username"]
        psw: str = request.form["password"]
        telegram_id: str = request.form["telegram-id"]
        token: str = request.form["token"]

        # If the token field is empty
        if len(token) == 0:  # user creates a new group
            if asyncio.run(registration_validation(username, psw, telegram_id)):
                telegram_id: int = int(telegram_id)  # if registration_validator is passed, then it is int
                psw_salt: str = get_salt()  # generating salt for a new user
                dbase = DatabaseQueries(connect_db_flask_g())
                user_token: str = dbase.create_new_group(telegram_id)  # we get token of the newly created group
                group_id: int = dbase.get_group_id_by_token(user_token)
                create_table_group(f"budget_{group_id}")

                """
                if an error occurred while defining the variables above, 
                then no further actions will be performed, 
                since add_user_to_db() will return False
                """
                if dbase.add_user_to_db(username, psw_salt, getting_hash(psw, psw_salt), group_id, telegram_id):
                    session.pop("userLogged", None)  # reset old cookies when registering a new user
                    logger_app.info(f"Successful registration: {username}. New group created: id={group_id}.")
                    flash("Registration completed successfully!", category="success")
                    flash(f"{username}, your token: {user_token}", category="success_token")
                else:
                    logger_app.error(f"Error registering user with new group. Group ID: {group_id}, "
                                     f"username: {username}, telegram ID: {telegram_id}, "
                                     f"get_salt status: {len(psw_salt) == 32}, "
                                     f"add_user_to_db return: {dbase.add_user_to_db(username, psw_salt, 
                                                               getting_hash(psw, psw_salt), group_id, telegram_id)}")
                    flash("Unknown error while creating account. Please contact technical support!", category="error")

        # User is added to an existing group
        elif len(token) == 32 and token.isalnum():  # token consists only of letters and numbers
            if asyncio.run(registration_validation(username, psw, telegram_id)):
                dbase = DatabaseQueries(connect_db_flask_g())
                group_id: int = dbase.get_group_id_by_token(token)
                group_not_full: bool = dbase.check_limit_users_in_group(group_id)  # checking places in the group

                if group_not_full:  # if the group doesn't exist, group_not_full will be set to False in the try/except
                    telegram_id: int = int(telegram_id)  # if registration_validator is passed, then it is int
                    psw_salt: str = get_salt()  # generating salt for a new user

                    if dbase.add_user_to_db(username, psw_salt, getting_hash(psw, psw_salt), group_id, telegram_id):
                        flash("Registration completed successfully!", category="success")
                        logger_app.info(f"Successful registration: {username}. Group: id={group_id}.")
                    else:
                        logger_app.info(f"Failed authorization  attempt: username = {username}, token = {token}.")
                        flash("Error creating user. Please try again and if the problem persists, "
                              "contact technical support.", category="error")
                else:
                    logger_app.info(f"The user entered an incorrect token or group is full: "
                                    f"username = {username}, token = {token}.")

                    flash("There is no group with this token or it is full. "
                          "Contact the group members for more information, or create your own group!",
                          category="error")

        # User made a mistake when entering the token
        elif len(token) > 0 and len(token) != 32:
            logger_app.info(f"The user entered a token of incorrect length: {token}.")
            flash("Error - token length must be 32 characters", category="error")

    return render_template("registration.html", title="Budget Graph - Registration")


@app.route('/login', methods=["GET", "POST"])  # send password in POST request and in hash
def login():
    session.permanent = True

    if "userLogged" in session:  # If the client has logged in before
        dbase = DatabaseQueries(connect_db_flask_g())
        username = session["userLogged"]
        user_is_exist: bool = dbase.check_username_is_exist(username)
        if user_is_exist:
            logger_app.info(f"Successful authorization (cookies): {session['userLogged']}.")
            return redirect(url_for("household", username=session["userLogged"]))
        else:
            session.pop("userLogged", None)  # removing the "userLogged" key from the session (browser cookies)
            flash("Your account was not found in the database. It may have been deleted.", category="error")
            logger_app.warning(f"Failed registration attempt from browser cookies: {username}")

    # here the POST request is checked, and the presence of the user in the database is checked
    if request.method == "POST":
        username: str = request.form["username"]
        psw: str = request.form["password"]
        dbase = DatabaseQueries(connect_db_flask_g())
        psw_salt: str = dbase.get_salt_by_username(username)

        if psw_salt and dbase.auth_by_username(username, getting_hash(psw, psw_salt)):
            session["userLogged"] = username
            dbase.update_user_last_login_by_username(username)
            logger_app.info(f"Successful authorization: {username}.")
            return redirect(url_for("household", username=session["userLogged"]))
        else:
            flash("This user doesn't exist.", category="error")
            logger_app.warning(f"Failed authorization attempt: {username}, user salt is exist: {len(psw_salt) != 0}")

    return render_template("login.html", title="Budget Graph - Login")


@app.route('/household/<username>', methods=["GET", "POST"])  # user's personal account
def household(username):
    """
    user's personal account with his group table
    """
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)

    dbase = DatabaseQueries(connect_db_flask_g())
    token: str = dbase.get_token_by_username(username)
    group_id: int = dbase.get_group_id_by_token(token)  # if token = "" -> group_id = 0

    if request.method == "POST":
        if "submit-button-1" in request.form or "submit-button-2" in request.form:  # Processing "Add to table" button
            value: str = request.form.get("transfer")
            value: int = value_validation(value)
            last_total_sum: int = dbase.get_last_sum_in_group(group_id)
            record_date: str = request.form.get("record-date")
            record_date: str = f"{record_date[-2:]}/{record_date[5:7]}/{record_date[:4]}"  # YYYY-MM-DD -> DD/MM/YYYY
            record_date_is_valid: bool = asyncio.run(date_validation(record_date))
            category: str = request.form.get("category")
            description = request.form.get("description")
            if "submit-button-2" in request.form:  # If this is an expense category
                value *= -1

            if not value:
                flash("The value format is invalid", category="error")

            elif not record_date_is_valid:
                flash("Date format is invalid", category="error")

            elif not description_validation(description):
                flash("Description format is invalid", category="error")

            elif not dbase.add_monetary_transaction_to_db(username, group_id, value, last_total_sum, record_date,
                                                          category, description):
                logger_app.error(f"Error adding data to database: "
                                 f"operation: {request.form}"
                                 f"table: budget_{group_id}")
                flash("Error adding data to database", category="error")
            else:
                flash("Data added successfully.", category="success")
        elif "delete-record-submit-button" in request.form:
            record_id: str = request.form.get("record-id")
            record_id: int = value_validation(record_id)

            if not record_id or not dbase.check_record_id_is_exist(group_id, record_id):
                flash("Error. The format of the entered data is incorrect.", category="error")
            elif not dbase.delete_budget_entry_by_id(group_id, record_id):
                logger_app.error(f"Error deletion record from database: table: budget_{group_id}, "
                                 f"username: {username}, record id: {record_id}.")
                flash("Error deleting a record from the database. Check that the entered data is correct.",
                      category="error")
            else:
                flash("Record successfully deleted", category="success")

    category_list: tuple[str, ...] = ("Supermarkets", "Restaurants", "Clothes", "Medicine", "Transport", "Devices",
                                      "Education", "Services", "Travel", "Housing", "Transfers", "Investments", "Hobby",
                                      "Jewelry", "Sale", "Salary", "Other")
    headers: tuple[str, ...] = ("№", "Total", "Username", "Transfer", "Category", "Date", "Description")
    data: tuple = dbase.select_data_for_household_table(group_id, 15)  # In case of error group_id == 0 -> data = []

    return render_template("household.html",
                           title=f"Budget Graph - {username}",
                           token=token,
                           username=username,
                           data=data,
                           headers=headers,
                           category_list=category_list)


@app.route('/settings/<username>')
def settings(username):
    """
    page with account and group settings (view/edit/delete)
    """
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)

    dbase = DatabaseQueries(connect_db_flask_g())
    token: str = dbase.get_token_by_username(username)
    group_id: int = dbase.get_group_id_by_token(token)
    group_owner: str = dbase.get_group_owner_username_by_group_id(group_id)
    group_users_data: list = dbase.get_group_users_data(group_id)

    return render_template("settings.html", title=f"Settings - {username}", token=token,
                           group_owner=group_owner, group_users_data=group_users_data)


@app.route('/about_premium')
def about_premium():
    return render_template("about_premium.html", title="About the premium subscription")


@app.route('/conditions')
def conditions():
    """
    privacy Policy page
    """
    return render_template("conditions.html",
                           title="Usage Policy",
                           site_name="",
                           site_url="",
                           contact_email="",
                           contact_url="")


@app.route('/logout', methods=['GET'])
def logout():
    """
    removing session from browser cookies
    """
    logger_app.info(f"Successful logout: {session['userLogged']}.")
    session.pop("userLogged", None)  # removing the "userLogged" key from the session (browser cookies)
    return redirect(url_for('login'))  # redirecting the user to another page, such as the homepage


@app.errorhandler(401)
def page_not_found(error):  # DO NOT REMOVE the parameter  # noqa
    return render_template("error401.html", title="UNAUTHORIZED"), 401


@app.errorhandler(404)
def page_not_found(error):  # DO NOT REMOVE the parameter  # noqa
    return render_template("error404.html", title="PAGE NOT FOUND"), 404


app.run(debug=True, host='0.0.0.0')  # change on False before upload on server
