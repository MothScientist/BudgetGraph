"""
This package is used to switch localization in the chatbot.
Also stores emoji and sticker codes for use inside the bot.
"""
from json import loads
from functools import cache
from os import path, listdir

from budget_graph.logger import setup_logger

logger_dict = setup_logger("logs/DictLog.log", "dict_loger")


class Emoji:
    __emoji_codes: dict = \
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
    @cache
    def get_emoji(emoji):
        return Emoji.__emoji_codes.get(emoji)


class Stickers:
    __stickers: dict = \
        {
            "id_1": "CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE",
            "id_2": "CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE",
            "id_3": "CAACAgIAAxkBAAEKWillDGfSs-fnAAGchbLPICSILmW_7yoAAiMUAAKtXgABSjhqQKnHD7SIMAQ",
            "id_4": "CAACAgIAAxkBAAEKWitlDGgsUhrqGudQPNuk-nI8yiz53wACsRcAAlV9AUqXI5lmIbo_TzAE",
            "id_5": "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ"
        }

    @staticmethod
    @cache
    def get_sticker_by_id(sticker_id):
        return Stickers.__stickers.get(sticker_id)


@cache
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
    return str(dict_language_obj.get(phrase, 'Error'))


@cache
def get_translate_from_json(language: str) -> dict:
    """
    This function works with reading JSON files
    """
    localization_dir_path: str = path.join(path.dirname(__file__), f"localization/{language}.json")
    try:
        with open(localization_dir_path, encoding='utf-8') as json_file:
            json_dict: str = json_file.read()
        return loads(json_dict)
    except FileNotFoundError:
        logger_dict.error(f'Dictionary not found: {language}')
        return {}


@cache
def get_list_languages() -> tuple:
    """
    Returns a list of available languages
    """
    # some dictionaries already exist, but are not yet available to users
    list_of_excluded_languages: tuple = ()
    localization_dir_path: str = path.join(path.dirname(__file__), 'localization')
    lang_json: list = [file[:2] for file in listdir(localization_dir_path)
                       if file.endswith('.json') and file[:2] not in list_of_excluded_languages]
    lang_json.sort()
    return tuple(lang_json)
