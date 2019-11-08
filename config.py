# -*- coding:utf-8 -*-

SECRET_KEY = 'very_very_secure_and_secret'
# Flask-Mail
MAIL_SERVER = 'smtp.mail.ru'
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = 'test@mail.ru'
MAIL_PASSWORD = '1234567890'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

