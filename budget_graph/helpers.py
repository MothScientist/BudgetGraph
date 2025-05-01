"""
Methods for the bot to work, mainly keyboard caching
"""
from sys import path as sys_path
from functools import cache
from telebot.types import InlineKeyboardButton, BotCommand

sys_path.append('../')
from budget_graph.global_config import GlobalConfig
from budget_graph.dictionary import receive_translation


class StorageMsgIdForDeleteAfterOperation:
	"""
	Stores message IDs that are deleted after a transaction is completed (the option is enabled in the user settings)
	"""
	def __init__(self, feature_is_active=None):
		self.feature_is_active: bool = feature_is_active
		self.msg_id_to_delete: list = []

	def append(self, msg_id: int):
		if self.feature_is_active and msg_id not in self.msg_id_to_delete:
			self.msg_id_to_delete.append(msg_id)

	def delete_messages(self, bot, chat_id: int) -> None:
		"""
		:param bot: bot object through which messages can be deleted
		:param chat_id:
		"""
		if self.feature_is_active:
			bot.delete_messages(chat_id, self.msg_id_to_delete)


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
def get_language_buttons() -> tuple:
	return (
		[InlineKeyboardButton('English', callback_data='change_language_en')],
		[InlineKeyboardButton('Español', callback_data='change_language_es')],
		[InlineKeyboardButton('Русский', callback_data='change_language_ru')],
		[InlineKeyboardButton('Français', callback_data='change_language_fr')],
		[InlineKeyboardButton('Deutsch', callback_data='change_language_de')],
		[InlineKeyboardButton('Islenskur', callback_data='change_language_is')],
		[InlineKeyboardButton('Português', callback_data='change_language_pt')],
		[InlineKeyboardButton('қазақ', callback_data='change_language_kk')]
	)


@cache
def get_diagram_buttons(user_language: str, user_is_owner: bool, user_is_premium: bool) -> tuple:
	return_buttons: list = []
	buttons: tuple = (
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'my_budget_diagram'), callback_data='get_diagram_0'
			)  # premium
		],
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'budget_diagram_for_group'), callback_data='get_diagram_1'
			)  # group_owner
		],
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'specific_user_budget_diagram'), callback_data='get_diagram_2'
			)  # group_owner + premium
		],
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'get_diagram_info'), callback_data='get_diagram_info'
			)  # for any user
		]
	)
	# It is important that the buttons are in their original order.
	if user_is_premium:
		return_buttons.append(buttons[0])
	if user_is_owner:
		return_buttons.append(buttons[1])
		if user_is_premium:
			return_buttons.append(buttons[2])
	return_buttons.append(buttons[-1])
	return tuple(return_buttons)


@cache
def get_premium_buttons(user_language: str, premium_status: bool) -> tuple:
	premium_buttons: tuple = (
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'get_premium'), callback_data='premium_get'
			)
		],
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'check_premium_status'), callback_data='premium_status'
			)
		],
		[
			InlineKeyboardButton(
				receive_translation(user_language, 'about_premium'), callback_data='premium_info'
			)
		]
	)
	if premium_status:
		return tuple(premium_buttons[1:])
	return tuple(premium_buttons[0:3:2])


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

	# pylint: disable=expression-not-assigned
	[rows.append(buttons_timezone_negative[i: i + row_width]) for i in range(0, 12, row_width)]  # append
	rows.append([InlineKeyboardButton('UTC', callback_data='change_timezone_0')])
	# pylint: disable=expression-not-assigned
	[rows.append(buttons_timezone_positive[j: j + row_width]) for j in range(0, 12, row_width)]  # append

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
	commands: list = [
		BotCommand('start', 'Start'),
		BotCommand('help', 'Help'),
		BotCommand('premium', 'Premium'),
		BotCommand('change_language', 'Change Language'),
		BotCommand('del_msg_after_transaction', '[ON/OFF] Delete messages after successful transaction'),
		BotCommand('skip_input_date', '[ON/OFF] Skip setting transaction date (current will be used)'),
		BotCommand('skip_input_category', '[ON/OFF] Skip transaction category selection'),
		BotCommand('skip_input_description', '[ON/OFF] Skip adding description to transaction'),
		BotCommand('change_timezone', 'Change Time zone'),
		BotCommand('get_my_id', 'Get my Telegram ID'),
		BotCommand('project_github', 'GitHub')
	]

	if GlobalConfig.localization_enable:
		commands.insert(1, BotCommand('change_language', 'Change Language'))

	return commands
