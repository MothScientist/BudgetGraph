"""
The file is run as a script after the main application is deployed, it populates the cache, for example, localization
"""
from json import load

from dictionary import get_list_languages, get_translate_from_json, receive_translation


def fill_localization_cache() -> None:
	list_languages = get_list_languages()

	with open(f'../budget_graph/localization/{list_languages[0]}.json', encoding='utf-8') as language_json_file:
		keys_data = load(language_json_file)
	all_keys: list = list(keys_data.keys())

	# we make a call to each phrase for each language, the rest of the functions will be cached inside the call
	for lang in list_languages:
		for phrase in all_keys:
			receive_translation(lang, phrase)


if __name__ == '__main__':
	fill_localization_cache()
