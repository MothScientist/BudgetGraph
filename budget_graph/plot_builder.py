from os import getenv
from uuid import UUID
from requests import post
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
host = getenv('PLOT_BUILDER_HOST')
port = getenv('PLOT_BUILDER_PORT')


def send_report_request(data: dict[str, tuple | list], uuid: UUID | str) -> bool | None:
    """
    :param data: {"username_1": (float(income sum), float(expense sum)), "username_2": etc.}
    :param uuid: uuid4()
    Sending a request with data to the server deployed on the main application machine (local server)    """
    if not isinstance(uuid, (UUID, str)) or not data or not all(len(elem) == 2 for elem in data.values()):
        return

    json_data = {
        "data": data,
        "uuid": str(uuid)
    }
    return post(f'http://{host}:{port}/generate', json=json_data).status_code == 200
