bind = "127.0.0.1:8000"
workers = 3
chdir = '/var/www/backend/aroma-stroy-react/backend/houses'
raw_env = 'DJANGO_SETTINGS_MODULE=houses.settings'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'
ALLOWED_HOSTS = ("aroma-stroy.by","127.0.0.1",)