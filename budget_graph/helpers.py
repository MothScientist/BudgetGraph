"""
Auxiliary methods
"""
from sys import path as sys_path
from functools import cache

sys_path.append('../')
from budget_graph.dictionary import receive_translation


@cache
def get_category_button_labels(user_language: str) -> tuple:
	"""
	receive_translation has caching,
	but since there are quite a lot of calls here,
	it is easier for us to cache the entire tuple at once
	"""
	return (
		receive_translation(user_language, "supermarkets"),
		receive_translation(user_language, "restaurants"),
		receive_translation(user_language, "clothes"),
		receive_translation(user_language, "medicine"),
		receive_translation(user_language, "transport"),
		receive_translation(user_language, "devices"),
		receive_translation(user_language, "education"),
		receive_translation(user_language, "services"),
		receive_translation(user_language, "travel"),
		receive_translation(user_language, "housing"),
		receive_translation(user_language, "transfer"),
		receive_translation(user_language, "investments"),
		receive_translation(user_language, "hobby"),
		receive_translation(user_language, "jewelry"),
		receive_translation(user_language, "salary"),
		receive_translation(user_language, "charity"),
		receive_translation(user_language, "other")
	)