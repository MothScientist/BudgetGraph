"""
This package is used to switch localization in the chatbot.
Also stores emoji and sticker codes for use inside the bot.
"""
from json import loads
from functools import cache
from os import path as os_path, listdir

from budget_graph.logger import setup_logger
from budget_graph.global_config import GlobalConfig

logger_dict = setup_logger('logs/DictLog.log', 'dict_loger')


class Emoji:
    __emoji_codes: dict = \
        {
            'robot':       129302,  # 🤖
            'key':         128273,  # 🔑
            'book':        128214,  # 📖
            'diagram':     128202,  # 📊
            'hourglass':   9203,    # ⏳
            'income':      128200,  # 📈
            'expense':     128201,  # 📉
            'delete':      10060,   # ❌
            'unload':      128228,  # 📤
            'earth':       127757,  # 🌍
            'stop':        128683,  # 🚫
            'money':       128181,  # 💵
            'money_wings': 128184,  # 💸
            'premium':     11088,   # ⭐
            'dollar':      128178,  # 💲
            'lock':        128272,  # 🔐
            'back':        128281,  # 🔙
            'magic':       129668,  # 🪄
            'sun':         127765,  # 🌕
            'moon':        127761,  # 🌑
            'yes':         128077,  # 👍
            'no':          128078,  # 👎
        }

    @staticmethod
    @cache
    def get_emoji(emoji: str) -> str:
        return chr(Emoji.__emoji_codes.get(emoji, 10067))  # question mark if not found


class Stickers:
    __stickers: dict = \
        {
            'id_1': 'CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE',
            'id_2': 'CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE',
            'id_3': 'CAACAgIAAxkBAAEKWillDGfSs-fnAAGchbLPICSILmW_7yoAAiMUAAKtXgABSjhqQKnHD7SIMAQ',
            'id_4': 'CAACAgIAAxkBAAEKWitlDGgsUhrqGudQPNuk-nI8yiz53wACsRcAAlV9AUqXI5lmIbo_TzAE',
            'id_5': 'CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ'
        }

    @staticmethod
    @cache
    def get_sticker_by_id(sticker_id) -> str:
        return Stickers.__stickers.get(sticker_id, '')


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
    if language not in get_list_languages():
        return 'Error'

    # if localization is disabled - the default language is English
    dict_language_obj: dict = get_translate_from_json(language if GlobalConfig.localization_enable else 'en')

    return str(dict_language_obj.get(phrase, 'Error'))


@cache
def get_translate_from_json(language: str) -> dict:
    """
    This function works with reading JSON files
    """
    localization_dir_path: str = os_path.join(os_path.dirname(__file__), f'localization/{language}.json')
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
    localization_dir_path: str = os_path.join(os_path.dirname(__file__), 'localization')
    lang_json: list = [file[:2] for file in listdir(localization_dir_path)
                       if file.endswith('.json') and file[:2] not in list_of_excluded_languages]
    lang_json.sort()  # so that the order always remains the same
    return tuple(lang_json)
