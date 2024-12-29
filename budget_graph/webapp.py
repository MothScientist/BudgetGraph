import os
import sys
import asyncio
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort


sys.path.append('../')

from budget_graph.logger import setup_logger
from budget_graph.registration_service import user_registration
from budget_graph.encryption import getting_hash, get_salt, logging_hash
from budget_graph.db_manager import connect_db_flask_g, close_db_flask_g, DatabaseQueries
from budget_graph.validation import value_validation, description_validation, date_validation, registration_validation

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config.from_object(__name__)

# Get the secret key to encrypt the Flask session from an environment variable
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

app.teardown_appcontext(close_db_flask_g)  # Disconnects the database connection after a query

# session lifetime in browser cookies
app.permanent_session_lifetime = timedelta(days=7)  # timedelta from datetime module

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
        res = asyncio.run(registration_validation(username, psw, telegram_id))
        if res[0]:
            registration_process(int(telegram_id), username, psw, token if token else 'None')
        elif res[1] == 1:
            flash("Error - invalid username format. Use 3 to 20 characters.", category="error")
        elif res[1] == 2:
            flash("Error - invalid password format. Use 8-32 characters / at least 1 number and 1 letter",
                  category="error")
        elif res[1] == 3:
            flash("Error - invalid telegram ID.", category="error")
    return render_template("registration.html", title="Budget Graph - Registration")


def registration_process(telegram_id: int, username: str, psw: str, token: str) -> None:
    psw_salt: str = get_salt()
    psw_hash: str = getting_hash(psw, psw_salt)
    connection = connect_db_flask_g()
    res, status = user_registration(DatabaseQueries(connection), token, telegram_id, username, psw_salt, psw_hash)

    if res:
        flash("Registration completed successfully!", category="success")
        if status:
            flash(f"{username}, your token: {status}", category="success_token")
        return

    if status == 'create_new_user_or_group_error':
        logger_app.info(f"Failed authorization  attempt: username = {logging_hash(username)}, "
                        f"token = {token}.")
        flash("Error creating user. Please try again and if the problem persists, "
              "contact technical support.", category="error")
    elif status == 'group_not_exist':
        logger_app.info(f"The user entered an incorrect token or group is full: "
                        f"username = {logging_hash(username)}, token = {token}.")
        flash("This group has a maximum number of users. Contact the group owner for a solution!",
              category="error")
    elif status == 'group_is_full':
        logger_app.info(f"The user entered an incorrect token: "
                        f"username = {logging_hash(username)}, token = {token}.")
        flash("There is no group with this token. Please check your details or contact the group owner!",
              category="error")
    elif status == 'invalid_token_format':
        logger_app.info(f"The user entered a token of incorrect length: {token}.")
        flash("Error - token length must be 32 characters", category="error")
    return


@app.route('/login', methods=["GET", "POST"])  # send password in POST request and in hash
def login():
    session.permanent = True

    if "userLogged" in session:  # If the client has logged in before
        dbase = DatabaseQueries(connect_db_flask_g())
        username = session["userLogged"]
        user_is_exist: bool = dbase.check_username_is_exist(username)
        if user_is_exist:
            logger_app.info(f"Successful authorization (cookies) -> username: {logging_hash(username)}")
            return redirect(url_for("household", username=username))
        session.pop("userLogged", None)  # removing the "userLogged" key from the session (browser cookies)
        flash("Your account was not found in the database. It may have been deleted.", category="error")
        logger_app.warning(f"Failed registration attempt from browser cookies -> "
                           f"username: {logging_hash(username)}")

    # here the POST request is checked, and the presence of the user in the database is checked
    if request.method == "POST":
        username: str = request.form["username"]
        psw: str = request.form["password"]
        dbase = DatabaseQueries(connect_db_flask_g())
        psw_salt: str = dbase.get_salt_by_username(username)

        if psw_salt and dbase.auth_by_username(username, getting_hash(psw, psw_salt)):
            session["userLogged"] = username
            telegram_id: int = dbase.get_telegram_id_by_username(username)
            dbase.update_user_last_login_by_telegram_id(telegram_id)
            logger_app.info(f"Successful authorization: username: {logging_hash(username)}.")
            return redirect(url_for("household", username=session["userLogged"]))
        flash("This user doesn't exist.", category="error")
        logger_app.warning(f"Failed authorization attempt: username: {logging_hash(username)}, "
                           f"user salt is exist: {len(psw_salt) != 0}")

    return render_template("login.html", title="Budget Graph - Login")


# TODO - too-many-branches
# pylint: disable=too-many-branches
@app.route('/household/<username>', methods=["GET", "POST"])  # user's personal account
def household(username):
    """
    user's personal account with his group table
    """
    if "userLogged" not in session or session["userLogged"] != username:
        abort(401)

    dbase = DatabaseQueries(connect_db_flask_g())
    token, group_id = dbase.get_group_id_token_by_username(username)
    if request.method == "POST":
        if "submit-button-1" in request.form or "submit-button-2" in request.form:  # Processing "Add to table" button
            value: str = request.form.get("transfer")
            value: int = value_validation(value)

            record_date: str = request.form.get("record-date")
            record_date: str = f"{record_date[-2:]}/{record_date[5:7]}/{record_date[:4]}"  # YYYY-MM-DD -> DD/MM/YYYY

            category: str = request.form.get("category")
            description = request.form.get("description")

            record_date_is_valid: bool = asyncio.run(date_validation(record_date))
            description_is_valid: bool = description_validation(description)

            if "submit-button-2" in request.form:  # if this is an expense category
                value *= -1

            if not value:
                flash("The value format is invalid", category="error")

            elif not record_date_is_valid:
                flash("Date format is invalid", category="error")

            elif not description_is_valid:
                flash("Description format is invalid", category="error")

            # Sending a transaction
            elif not dbase.add_transaction_to_db(username, value, record_date, category, description):
                flash("Error adding data to database", category="error")

            else:  # If all checks are successful
                flash("Data added successfully.", category="success")

        elif "delete-record-submit-button" in request.form:
            record_id: str = request.form.get("record-id")
            record_id: int = value_validation(record_id)

            if not record_id or not dbase.check_record_id_is_exist(group_id, record_id):
                flash("Error. The format of the entered data is incorrect.", category="error")

            elif not dbase.process_delete_transaction_record(group_id, record_id):
                logger_app.error(f"Error deletion record from database: group #{group_id}, "
                                 f"username: {logging_hash(username)}, record id: {record_id}.")
                flash("Error deleting a record from the database. Check that the entered data is correct.",
                      category="error")

            else:
                flash("Record successfully deleted", category="success")

    category_list: tuple[str, ...] = ("Supermarkets", "Restaurants", "Clothes", "Medicine", "Transport", "Devices",
                                      "Education", "Services", "Travel", "Housing", "Transfers", "Investments",
                                      "Hobby", "Jewelry", "Sale", "Salary", "Other")
    headers: tuple[str, ...] = ("№", "Username", "Transfer", "Total", "Date", "Category", "Description")
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
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    dbase = DatabaseQueries(connect_db_flask_g())
    token, group_id = dbase.get_group_id_token_by_username(username)
    group_owner: str = dbase.get_group_owner_username_by_group_id(group_id)
    group_users_data: list = dbase.get_group_users_data(group_id)

    return render_template('settings.html', title=f'Settings - {username}', token=token,
                           group_owner=group_owner, group_users_data=group_users_data)


@app.route('/about_premium')
def about_premium():
    return render_template('about_premium.html', title='About the premium subscription')


@app.route('/conditions')
def conditions():
    """
    privacy Policy page
    """
    return render_template(
        'conditions.html',
        title='Usage Policy',
        site_name='',
        site_url='',
        contact_email='',
        contact_url=''
    )


@app.route('/logout', methods=['GET'])
def logout():
    """
    removing session from browser cookies
    """
    logger_app.info(f"Successful logout: username: {logging_hash(session['userLogged'])}.")
    session.pop('userLogged', None)  # removing the "userLogged" key from the session (browser cookies)
    return redirect(url_for('login'))  # redirecting the user to another page, such as the homepage


# pylint: disable=unused-argument
@app.errorhandler(401)
def page_not_found_401(error):  # DO NOT REMOVE the parameter  # noqa
    return render_template('error401.html', title='UNAUTHORIZED'), 401


# pylint: disable=unused-argument
@app.errorhandler(404)
def page_not_found_404(error):  # DO NOT REMOVE the parameter  # noqa
    return render_template("error404.html", title="PAGE NOT FOUND"), 404


app.run(debug=True, host='0.0.0.0')  # change on False before upload on server
