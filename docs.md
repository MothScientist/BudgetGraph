# No relevant for the current version of the project!
## **Disclaimer**
All functions in this manual are described with abbreviations and simplified syntax - this is necessary to improve understanding of the principles of the project.</br></br>
For a more accurate understanding, please look directly at these functions themselves in the project source code.

### Logging

#### How does the log settings function work?

We are talking about the ```setup_logger``` function in the ```log_settings.py``` file.</br></br>
At the beginning we check the presence of a directory for storing log files:
```python3
import os

if not os.path.exists("logs"):
    os.makedirs("logs")
```
if this directory does not exist, then it will be created when one of the project applications is restarted, or when the database is created.

Next, we create a unique logger that will send logs to the file we specified:
```python3
logger = logging.getLogger(logger_name)
```

Below we indicate the maximum file size and how many files can be created (if full, the old ones will be deleted):
```python3
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
```

Then we indicate the formatting we need:
```python3
from logging import Formatter

formatter = Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
```
Example of the final log:
```log
2020-01-01 12:30:00,000 DEBUG: Database connection (main): OK [in /home/user/project/main/database_control.py:348]
```

With the following lines we check whether this logger has its own handler, if not, then we assign it:
```python3
if not logger.hasHandlers():
    logger.addHandler(handler)
```

### @timeit
A decorator required at the development stage. Useful for code optimization, helps to find unexpected errors in the code. When actually using the project, it is necessary to comment it out, as this affects performance due to unnecessary calculations.

Collects data on the operating time of functions in a log file.
```python3
from log_settings import setup_logger
import time
from functools import wraps

logger_time = setup_logger("logs/TimeLog.log", "time_logger")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _start = time.perf_counter()
        result = func(*args, **kwargs)
        _end = time.perf_counter()
        logger_time.info(f'{func.__name__}: {_end - _start:.6f} sec.')
        return result

    return wrapper

@timeit
def func(*args):
    pass
```
Thus, it allows you to collect data on the speed of function execution in a log file, and then use this data to improve the performance of your code.

### Registration
#### Bot
The first function checks whether the user is already registered and accidentally got into this menu.</br>
Because we assume that the user should enter this menu exactly 1 time.
```python3
@bot.message_handler(commands=['registration'])
def registration(message) -> None:
    res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
    
    if not res:
        bot.register_next_step_handler(message, process_username)
```
If not registered, then go to the username and its validation:
```python3
def process_username(message):

    if asyncio.run(username_validator(username)):
        bot.register_next_step_handler(message, process_psw, username)
```
```asyncio.run()``` applies because we are using an asynchronous function without having async.</br></br>
If validation is successful, we pass the username to the following function, which will accept the new user’s password and validate it:
```python3
def process_psw(message, username: str):

    if asyncio.run(password_validator(psw)):
        bot.register_next_step_handler(message, process_token, username, psw, psw_salt)
```
If the password is successfully validated, we pass the username and password to the following function:
```python3
def process_token(message, username: str, psw_hash: str, psw_salt: str):

    if compare_digest(token, "None"):
        if user_token := bot_db.create_new_group(telegram_id):
            group_id: int = token_validator(user_token)

            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                create_table_group(f"budget_{group_id}")
                bot.send_message(message.chat.id, "Congratulations on registering!")

    elif len(token) == 32:
        telegram_id: int = message.from_user.id

        if group_id := token_validator(token):
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                bot.send_message(message.chat.id, "Congratulations on registering!")

    else:
        bot.send_message(message.chat.id, "This is not a valid token format, please check if it is correct or send 'None'!")

```
3 options for accepted token
1. ```None``` - no token
2. ```len(token) == 32``` - checking the token for existence
3. ```else``` - errors when entering a token

#### Site
On the site, all registration functionality occurs within one function, calling the necessary validations and database methods.
```python3
@app.route('/registration', methods=["GET", "POST"])
def registration():
```
The difference from registration via a bot is that all 3 validations occur simultaneously and asynchronously:
```python3
asyncio.run(registration_validator(username, psw, telegram_id))
```
#### Validations:
```python3
async def username_validator(username: str) -> bool:
    username_is_unique = check_username_is_unique(username)

    if 3 <= len(username) <= 20 and re.match(r"^[a-zA-Z0-9]+$", username) and username_is_unique:
        return True

    else:
        return False


async def password_validator(psw: str) -> bool:
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,32}$', psw):
        return True
    else:
        return False


async def telegram_id_validator(telegram_id: str) -> bool:
    if re.match(r'^[1-9]\d{2,11}$', telegram_id):
        telegram_id: int = int(telegram_id)
    else:
        return False

    telegram_id_is_unique = check_telegram_id_is_unique(telegram_id)

    if telegram_id_is_unique:
        return True
    else:
        return False
```

### Login
#### Bot
Authorization in telegram occurs without user participation; when sending the /start command, we automatically check the presence of this telegram ID in the database.
```python3
telegram_id: int = message.from_user.id
res: bool | str = get_username_by_telegram_id(telegram_id)

    if res:
        update_user_last_login(res)
```
#### Site
First, we check the user session in the browser cookies
```python3
if "userLogged" in session:
    return redirect(url_for("household", username=session["userLogged"]))
```
If not, then we display the html registration page, where we then check the correctness of the entered data in accordance with the information stored in the database.
```python3
    if request.method == "POST":
        username: str = request.form["username"]
        psw: str = request.form["password"]
        token: str = request.form["token"
        psw_salt: str = get_salt_by_username(username)

        if psw_salt and auth_by_username(username, getting_hash(psw, psw_salt), token):

            session["userLogged"] = username
            update_user_last_login(username)
            return redirect(url_for("household", username=session["userLogged"]))
```