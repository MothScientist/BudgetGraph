import sys
sys.path.append("..")
sys.path.append("tests")
from manage_test_db import create_test_db

if __name__ == "__main__":
    create_test_db()
