# prod.py
# Production settings for myapp

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']
DEBUG = True #cuando es true static se saca de statics, si es falso se saca de collection

# Recuerda crear la carpeta logs en la raiz del proyecto

LOG_VIEWER_FILES = ['logfile1', 'logfile2', ...]
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = './logs/'
LOG_VIEWER_PAGE_LENGTH = 25       # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25 # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log from line

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "ERROR", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "./logs/django.log",
            "formatter": "app",
        },
        "fileRequest": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/django_request.log",
            "formatter": "app",
        },
        "fileDB": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/django_db.log",
            "formatter": "app",
        },
        "fileMenu": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/django_menu.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
        "django.request": {
            "handlers": ["fileRequest"],
            "level": "INFO",
            "propagate": True
        },
        "DBTienda": {
            "handlers": ["fileDB"],
            "level": "INFO",
            "propagate": True
        },
        "menuAndWelcome": {
            "handlers": ["fileMenu"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"[%(levelname)s] %(asctime)s "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}