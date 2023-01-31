# prod.py
# Production settings for myapp

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']
DEBUG = False #cuando es true static se saca de statics, si es falso se saca de collection
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "ERROR", "handlers": ["file"]},
    "handlers": {
        "console": {
            'class': 'logging.StreamHandler',
            'formatter': 'app',
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