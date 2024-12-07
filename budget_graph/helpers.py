"""
Auxiliary methods
"""
from sys import path as sys_path
from functools import cache
from telebot.types import InlineKeyboardButton, BotCommand

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
		receive_translation(user_language, 'supermarkets'),
		receive_translation(user_language, 'restaurants'),
		receive_translation(user_language, 'clothes'),
		receive_translation(user_language, 'medicine'),
		receive_translation(user_language, 'transport'),
		receive_translation(user_language, 'devices'),
		receive_translation(user_language, 'education'),
		receive_translation(user_language, 'services'),
		receive_translation(user_language, 'travel'),
		receive_translation(user_language, 'housing'),
		receive_translation(user_language, 'transfer'),
		receive_translation(user_language, 'investments'),
		receive_translation(user_language, 'hobby'),
		receive_translation(user_language, 'jewelry'),
		receive_translation(user_language, 'salary'),
		receive_translation(user_language, 'charity'),
		receive_translation(user_language, 'other')
	)


@cache
def get_timezone_buttons() -> tuple:
	buttons_timezone_negative: tuple = (
		InlineKeyboardButton('UTC-12', callback_data='change_timezone_-12'),
		InlineKeyboardButton('UTC-11', callback_data='change_timezone_-11'),
		InlineKeyboardButton('UTC-10', callback_data='change_timezone_-10'),
		InlineKeyboardButton('UTC-9', callback_data='change_timezone_-9'),
		InlineKeyboardButton('UTC-8', callback_data='change_timezone_-8'),
		InlineKeyboardButton('UTC-7', callback_data='change_timezone_-7'),
		InlineKeyboardButton('UTC-6', callback_data='change_timezone_-6'),
		InlineKeyboardButton('UTC-5', callback_data='change_timezone_-5'),
		InlineKeyboardButton('UTC-4', callback_data='change_timezone_-4'),
		InlineKeyboardButton('UTC-3', callback_data='change_timezone_-3'),
		InlineKeyboardButton('UTC-2', callback_data='change_timezone_-2'),
		InlineKeyboardButton('UTC-1', callback_data='change_timezone_-1'),
	)

	buttons_timezone_positive: tuple = (
		InlineKeyboardButton('UTC+12', callback_data='change_timezone_12'),
		InlineKeyboardButton('UTC+11', callback_data='change_timezone_11'),
		InlineKeyboardButton('UTC+10', callback_data='change_timezone_10'),
		InlineKeyboardButton('UTC+9', callback_data='change_timezone_9'),
		InlineKeyboardButton('UTC+8', callback_data='change_timezone_8'),
		InlineKeyboardButton('UTC+7', callback_data='change_timezone_7'),
		InlineKeyboardButton('UTC+6', callback_data='change_timezone_6'),
		InlineKeyboardButton('UTC+5', callback_data='change_timezone_5'),
		InlineKeyboardButton('UTC+4', callback_data='change_timezone_4'),
		InlineKeyboardButton('UTC+3', callback_data='change_timezone_3'),
		InlineKeyboardButton('UTC+2', callback_data='change_timezone_2'),
		InlineKeyboardButton('UTC+1', callback_data='change_timezone_1'),
	)

	rows: list = []
	row_width: int = 4

	[rows.append(buttons_timezone_negative[i: i + row_width]) for i in range(0, 12, row_width)]
	rows.append([InlineKeyboardButton('UTC', callback_data='change_timezone_0')])
	[rows.append(buttons_timezone_positive[j: j + row_width]) for j in range(0, 12, row_width)]

	return tuple(rows)


@cache
def get_category_translate(user_language: str) -> tuple:
	return (
		receive_translation(user_language, 'username'),
		receive_translation(user_language, 'transfer'),
		receive_translation(user_language, 'total'),
		receive_translation(user_language, 'datetime'),
		receive_translation(user_language, 'category'),
		receive_translation(user_language, 'description')
	)


def get_bot_commands() -> list:
	return [
		BotCommand('start', 'Start'),
		BotCommand('change_language', 'Change Language'),
		BotCommand('change_timezone', 'Change Time zone'),
		BotCommand('get_my_id', 'Get my Telegram ID'),
		BotCommand('premium', 'Premium'),
		BotCommand('help', 'Help'),
		BotCommand('project_github', 'GitHub')
	]
