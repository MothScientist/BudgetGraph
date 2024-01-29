import sys

sys.path.append('../')

from tests.manage_test_db import create_test_db
from os import makedirs

if __name__ == "__main__":
    create_test_db()
    makedirs("logs", exist_ok=True)
