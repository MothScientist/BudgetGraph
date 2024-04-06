"""
    This package is used to switch localization in the chatbot.

    Also stores emoji and sticker codes for use inside the bot.
"""
import json
from os import path
from app.logger import setup_logger

logger_dict = setup_logger("logs/DictLog.log", "dict_loger")


class Emoji:
    _emoji_codes: dict = \
        {
            "question": "",
            "clip": "",
            "laptop": "",
            "lock": "",
            "money": "",
            "book": "",
            "growing graph": "",
            "falling graph": "",
            "cross": "",
            "directory": "",
            "star": "",
            "earth": "",
            "basket": "",
            "key": "",
            "robot": ""
        }

    @staticmethod
    def get_emoji(emoji):
        return Emoji._emoji_codes.get(emoji)


class Stickers:
    _stickers: dict = \
        {
            "id_1": "CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE",
            "id_2": "CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE",
            "id_3": "CAACAgIAAxkBAAEKWillDGfSs-fnAAGchbLPICSILmW_7yoAAiMUAAKtXgABSjhqQKnHD7SIMAQ",
            "id_4": "CAACAgIAAxkBAAEKWitlDGgsUhrqGudQPNuk-nI8yiz53wACsRcAAlV9AUqXI5lmIbo_TzAE",
            "id_5": "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ"
        }

    @staticmethod
    def get_sticker_by_id(sticker_id):
        return Stickers._stickers.get(sticker_id)


def receive_translation(language: str, phrase: str) -> str:
    """
    The function takes as input a phrase that the chatbot responds to the user in the selected language
    (also passed in the parameters).
    These phrases are known in advance and are found along with translations in the localization dictionary.

    :param language: one of the valid language codes -> en / ru / es / fr / de / is.
    :param phrase: string that is a key in the language dictionary.
    :return: value in the json-dictionary in the selected language.
    """
    dict_language_obj: dict = get_translate_from_json(language)
    return dict_language_obj.get(phrase)


def get_translate_from_json(language: str) -> dict:
    """
    This function works with reading JSON files.
    """
    localization_dir_path: str = path.join(path.dirname(__file__), f"localization/{language}.json")
    try:
        with open(localization_dir_path, encoding='utf-8') as json_file:
            json_dict: str = json_file.read()
        return json.loads(json_dict)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    res = receive_translation("es", "data_is_safe")
    print(res)