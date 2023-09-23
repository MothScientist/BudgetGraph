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