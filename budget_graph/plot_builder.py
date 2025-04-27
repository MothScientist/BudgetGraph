from sys import path as sys_path
from os import getenv, remove
from uuid import UUID
from requests import post
from dotenv import load_dotenv

sys_path.append('../')
from budget_graph.logger import setup_logger
from budget_graph.db_manager import connect_defer_close_db

load_dotenv()  # Load environment variables from .env file
host = getenv('PLOT_BUILDER_HOST')
port = getenv('PLOT_BUILDER_PORT')

logger_report_request = setup_logger('logs/ReportRequestsLog.log', 'report_request_loger')


class Reports:
    """
    An object that accepts a report request. Sends a request to the go server and deletes outdated reports
    """
    await_list = {}
    diagram_to_delete = []

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
        if (not chat_id or not isinstance(uuid, (UUID, str))
                or not data or not all(len(elem) == 2 for elem in data.values())):
            logger_report_request.warning(f'Invalid data: chat_id: {chat_id}; uuid: {uuid}; data: {data}')
            return False
        json_data = {
            "data": data,
            "uuid": str(uuid)
        }
        status: bool = post(f'http://{host}:{port}/api/report/generate', json=json_data).status_code == 200
        if status:
            logger_report_request.info(f'Request sent successfully. chat_id: {chat_id}; uuid: {uuid}')
            Reports.await_list[uuid] = chat_id
            return True
        else:
            logger_report_request.warning(f'Error sending request. status: {status}; chat_id: {chat_id}; uuid: {uuid}')
            return False

    @staticmethod
    def delete_unused_diagram():
        files_to_delete = Reports.diagram_to_delete
        Reports.diagram_to_delete = []
        for uuid in files_to_delete:
            path: str = f'graphs/{uuid}.html'
            try:
                remove(path)
            except (FileNotFoundError, PermissionError) as err:
                logger_report_request.warning(f"Error deleting report: {err}. Path: {path};")
            finally:
                logger_report_request.info(f'The outdated report has been removed. Path: {path};')


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
