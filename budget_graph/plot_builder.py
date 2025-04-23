from sys import path as sys_path
from os import getenv
from uuid import UUID
from requests import post
from dotenv import load_dotenv

sys_path.append('../')
from budget_graph.db_manager import connect_defer_close_db

load_dotenv()  # Load environment variables from .env file
host = getenv('PLOT_BUILDER_HOST')
port = getenv('PLOT_BUILDER_PORT')


class Reports:
    """
    TODO
    """
    await_list = {}

    @staticmethod
    def send_report_request(
            chat_id: int, data: dict[str, tuple | list], uuid: UUID | str
    ) -> bool | None:
        """
        :param chat_id:
        :param data: {"username_1": (float(income sum), float(expense sum)), "username_2": etc.}
        :param uuid: uuid4()
        Sending a request with data to the server deployed on the main application machine (local server)
        """
        if not isinstance(uuid, (UUID, str)) or not data or not all(len(elem) == 2 for elem in data.values()):
            return False

        json_data = {
            "data": data,
            "uuid": str(uuid)
        }
        status: bool = post(f'http://{host}:{port}/generate', json=json_data).status_code == 200

        if status:
            Reports.await_list[uuid] = chat_id
            return True
        else:
            return False


@connect_defer_close_db
def build_diagram(db_connection, chat_id: int, telegram_id: int, uuid: UUID,  diagram_type: int) -> bool:
    """
    diagram_type:
        0 - по запросившему пользователю
        1 - по группе
        2 - по конкретному пользователю (доступно только владельцу группы)
    """
    data: dict[str, tuple] = db_connection.get_data_for_plot_builder(telegram_id, diagram_type)
    return Reports.send_report_request(chat_id, data, uuid) if data else None