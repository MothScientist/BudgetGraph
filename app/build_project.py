import sys

sys.path.append('../')

from app.database_control import create_db

if __name__ == '__main__':
    create_db()
