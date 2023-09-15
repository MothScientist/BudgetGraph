class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    LOGFILE = 'logs/Production.log'


class DevelopmentConfig(Config):
    DEBUG = True
    LOGFILE = 'logs/Development.log'
