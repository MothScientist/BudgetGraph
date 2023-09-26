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
    res: bool | str = bot_db.get_username_by_telegram_id(message.from_user.id)
    
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
...

### Login
#### Bot
...
#### Site
...