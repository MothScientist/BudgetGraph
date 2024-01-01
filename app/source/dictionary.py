"""
    This package is used to switch languages in the chatbot
"""
from log_settings import setup_logger

logger_dict = setup_logger("logs/SourceLog.log", "source_logger")


def receive_translation(language: str, phrase: str) -> str:  #FIXME
    """
    The function takes as input a phrase that the chatbot responds to the user in the selected language 
    (also passed in the parameters). 
    These phrases are known in advance and are found along with translations in the languages dictionary.

    Args:
        language (str): one of the valid language codes -> en / ru / es / fr / de / is
        phrase (str): string that is a key in the languages dictionary.

    Returns:
        str: value in the dictionary in the selected language
    """
    if language not in ["en", "ru", "es", "fr", "de", "is"]:
        logger_dict.warning("Language not recognized. language: %s", language)
        return languages["en"][phrase]
    return languages[language][phrase]


languages: dict = \
    {
        "en":
            {
                "misunderstanding": "I don't understand you :(",
                "greetings": "Hello",
                "our_user": "We recognized you. Welcome!",
                "unknown_user": "We didn't recognize you. Would you like to register in the project?",
                "help": "Help",
                "change_language": "Change the language",
                "language_changed": "Great!\nLanguage changed",
                "premium": "Premium",
                "link_github": "Link to GitHub",
                "click_need_button": "Click the button you need",
                "table_manage": "Table manage",
                "group_settings": "Group settings",
                "my": "My",
                "get_my_token": "Get my token",
                "register": "I want to register",
                "view_table": "View table",
                "add_income": "Add income",
                "add_expense": "Add expense",
                "del_record": "Delete record",
                "get_csv": "Get CSV-file",
                "back": "Back",
                "group_users": "Group users",
                "delete_account": "Delete my account",
                "delete_group": "Delete group",
                "change_owner": "Change owner",
                "delete_user": "Delete user",
                "your": "Your",
                "project_on_github": "Our open-source project on Github",
                "choose_language": "Choose a language"
            },

        "ru":
            {
                "misunderstanding": "Я вас не понимаю :(",
                "greetings": "Привет,",
                "our_user": "Мы узнали тебя. Добро пожаловать!",
                "unknown_user": "Мы вас не узнали. Не хотите зарегистрироваться в проекте?",
                "help": "Помощь",
                "change_language": "Изменить язык",
                "language_changed": "Отлично!\nЯзык изменён",
                "premium": "Премиум",
                "link_github": "Ссылка на Github",
                "click_need_button": "Нажмите нужную кнопку",
                "table_manage": "Управление таблицей",
                "group_settings": "Управление группой",
                "my": "Мой",
                "get_my_token": "Получить мой токен",
                "register": "Я хочу зарегистрироваться",
                "view_table": "Показать таблицу",
                "add_income": "Добавить доход",
                "add_expense": "Добавить расход",
                "del_record": "Удалить запись",
                "get_csv": "Получить CSV-файл",
                "back": "Назад",
                "group_users": "Пользователи группы",
                "delete_account": "Удалить мой аккаунт",
                "delete_group": "Удалить группу",
                "change_owner": "Сменить владельца",
                "delete_user": "Удалить пользователя",
                "your": "Ваш",
                "project_on_github": "Наш проект с открытым исходным кодом на Github",
                "choose_language": "Выберите язык",
            },

        "es":
            {
                "misunderstanding": "No lo comprendo :(",
                "greetings": "¡Hola",
                "our_user": "Te reconocimos. ¡Bienvenido!",
                "unknown_user": "No te reconocimos. ¿Quieres registrarte en el proyecto?",
                "help": "Ayuda",
                "change_language": "Cambia el idioma",
                "language_changed": "¡Excelente!\nIdioma cambiado",
                "premium": "de primera calidad",
                "link_github": "Enlace a GitHub",
                "click_need_button": "Haga clic en el botón que necesita",
                "table_manage": "Gestión de mesa",
                "group_settings": "Configuración de grupo",
                "my": "Mi",
                "get_my_token": "Obtener mi ficha",
                "register": "Quiero registrarme",
                "view_table": "Ver tabla",
                "add_income": "Agregar ingresos",
                "add_expense": "Agregar gasto",
                "del_record": "Eliminar el registro",
                "get_csv": "Obtener archivo CSV",
                "back": "Atrás",
                "group_users": "Usuarios del grupo",
                "delete_account": "Borrar mi cuenta",
                "delete_group": "Eliminar grupo",
                "change_owner": "Cambio de propietario",
                "delete_user": "Borrar usuario",
                "your": "Tu",
                "project_on_github": "Nuestro proyecto de código abierto en Github",
                "choose_language": "Elige un idioma",
            },

        "de":
            {
                "misunderstanding": "Ich verstehe Sie nicht :(",
                "greetings": "Hallo",
                "our_user": "Wir haben dich erkannt. Willkommen!",
                "unknown_user": "Wir haben dich nicht erkannt. Möchten Sie sich im Projekt registrieren?",
                "help": "Helfen",
                "change_language": "Ändere die Sprache",
                "language_changed": "Großartig!\nSprache geändert",
                "premium": "Prämie",
                "link_github": "Link zu GitHub",
                "click_need_button": "Klicken Sie auf die Schaltfläche, die Sie benötigen",
                "table_manage": "Tischverwaltung",
                "group_settings": "Gruppeneinstellungen",
                "my": "Mein",
                "get_my_token": "Holen Sie sich meinen Token",
                "register": "Ich möchte mich registrieren",
                "view_table": "Tabelle ansehen",
                "add_income": "Einkommen hinzufügen",
                "add_expense": "Kosten hinzufügen",
                "del_record": "Aufzeichnung löschen",
                "get_csv": "Holen Sie sich die CSV-Datei",
                "back": "Back",
                "group_users": "Gruppenbenutzer",
                "delete_account": "Mein Konto löschen",
                "delete_group": "Gruppe löschen",
                "change_owner": "Besitzer wechseln",
                "delete_user": "Benutzer löschen",
                "your": "Dein",
                "project_on_github": "Unser Open-Source-Projekt auf Github",
                "choose_language": "Wählen Sie eine Sprache",
            },

        "fr":
            {
                "misunderstanding": "Je ne te comprends pas :(",
                "greetings": "Bonjour",
                "our_user": "Nous vous avons reconnu. Accueillir!",
                "unknown_user": "Nous ne vous avons pas reconnu. Vous souhaitez vous inscrire au projet?",
                "help": "Aide",
                "change_language": "Changer la langue",
                "language_changed": "Super!\nLangue modifiée",
                "premium": "prime",
                "link_github": "Lien vers GitHub",
                "click_need_button": "Cliquez sur le bouton dont vous avez besoin",
                "table_manage": "Gestion des tables",
                "group_settings": "Paramètres du groupe",
                "my": "Mon / Ma",
                "get_my_token": "Récupérer mon jeton",
                "register": "Je veux m'inscrire",
                "view_table": "Voir le tableau",
                "add_income": "",
                "add_expense": "",
                "del_record": "",
                "get_csv": "",
                "back": "Back",
                "group_users": "",
                "delete_account": "",
                "delete_group": "",
                "change_owner": "",
                "delete_user": "",
                "your": "",
                "project_on_github": "",
                "choose_language": "",
            },

        "is":
            {
                "misunderstanding": "",
                "greetings": "",
                "our_user": "",
                "unknown_user": "",
                "help": "Hjálp",
                "change_language": "Breyttu tungumálinu",
                "language_changed": "Frábært!\nTungumál breytt",
                "premium": "yfirverði",
                "link_github": "Tengill á GitHub",
                "click_need_button": "",
                "table_manage": "",
                "group_settings": "",
                "my": "",
                "get_my_token": "",
                "register": "",
                "view_table": "",
                "add_income": "",
                "add_expense": "",
                "del_record": "",
                "get_csv": "",
                "back": "Back",
                "group_users": "",
                "delete_account": "",
                "delete_group": "",
                "change_owner": "",
                "delete_user": "",
                "your": "",
                "project_on_github": "",
                "choose_language": "",
            }
    }


emoji: dict = \
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
