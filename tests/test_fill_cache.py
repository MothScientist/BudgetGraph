from shutil import rmtree
import unittest
from time import perf_counter

from budget_graph.fill_cache import fill_localization_cache
from budget_graph.dictionary import receive_translation, get_list_languages, get_translate_from_json


class TestFillCache(unittest.TestCase):
	"""
	Testing that caching functions reduces their response time
	"""

	def test_fill_localization_cache_001(self):
		# delete all cache
		rmtree('../budget_graph/__pycache__', ignore_errors=True)
		rmtree('.pytest_cache', ignore_errors=True)
		rmtree('__pycache__', ignore_errors=True)

		time_first_call_start_list_lang: float = perf_counter()
		list_languages_1: tuple = get_list_languages()
		time_first_call_finish_list_lang: float = perf_counter()
		before_res_list_lang: float = time_first_call_finish_list_lang - time_first_call_start_list_lang

		time_first_call_start_json: float = perf_counter()
		for lang in list_languages_1:
			get_translate_from_json(lang)
		time_first_call_finish_json: float = perf_counter()
		before_res_json: float = time_first_call_finish_json - time_first_call_start_json

		keys_1: tuple = (
			"link_github", "get_my_token", "delete_group", "services", "enter_username", "create_new_user_error",
			"username", "current_owner_exception", "unknown_message", "unknown_user_in_group", "delete_table",
			"category", "set_date", "YES", "get_csv", "language_changed", "misunderstanding", "my"
		)
		time_first_call_start_translation: float = perf_counter()
		all(receive_translation(lang, _key) for _key in keys_1 for lang in list_languages_1)
		time_first_call_finish_translation: float = perf_counter()
		before_res_translation: float = time_first_call_finish_translation - time_first_call_start_translation

		# delete all cache
		rmtree('../budget_graph/__pycache__', ignore_errors=True)
		rmtree('.pytest_cache', ignore_errors=True)
		rmtree('__pycache__', ignore_errors=True)

		# cache all functions
		fill_localization_cache()

		time_first_call_start_list_lang: float = perf_counter()
		list_languages_2: tuple = get_list_languages()
		time_first_call_finish_list_lang: float = perf_counter()
		after_res_list_lang: float = time_first_call_finish_list_lang - time_first_call_start_list_lang

		time_first_call_start_json: float = perf_counter()
		for lang in list_languages_2:
			get_translate_from_json(lang)
		time_first_call_finish_json: float = perf_counter()
		after_res_json: float = time_first_call_finish_json - time_first_call_start_json

		keys_2: tuple = (
			"link_github", "get_my_token", "delete_group", "services", "enter_username", "create_new_user_error",
			"username", "current_owner_exception", "unknown_message", "unknown_user_in_group", "delete_table",
			"category", "set_date", "YES", "get_csv", "language_changed", "misunderstanding", "my"
		)
		time_first_call_start_translation: float = perf_counter()
		all(receive_translation(lang, _key) for _key in keys_2 for lang in list_languages_2)
		time_first_call_finish_translation: float = perf_counter()
		after_res_translation: float = time_first_call_finish_translation - time_first_call_start_translation

		self.assertTrue(
			after_res_list_lang < before_res_list_lang,
			f'before_res_list_lang = {before_res_list_lang}\n'
			f'after_res_list_lang = {after_res_list_lang}'
		)
		self.assertTrue(
			after_res_json < before_res_json,
			f'before_res_json = {before_res_json}\n'
			f'after_res_json = {after_res_json}'
		)
		self.assertTrue(
			after_res_translation < before_res_translation,
			f'before_res_translation = {before_res_translation}\n'
			f'after_res_translation = {after_res_translation}'
		)

	# look at the fact that the result is repeatable

	def test_fill_localization_cache_002(self):
		self.test_fill_localization_cache_001()

	def test_fill_localization_cache_003(self):
		self.test_fill_localization_cache_001()


if __name__ == '__main__':
	unittest.main()
