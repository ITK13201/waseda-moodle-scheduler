APP_NAME = "waseda-moodle-scheduler"
PORT = 8000

wsgi_app = "app.wsgi:application"
bind = "0.0.0.0:{}".format(PORT)
workers = 2

# log settings
accesslog = "/var/log/{}/access.log".format(APP_NAME)
errorlog = "/var/log/{}/error.log".format(APP_NAME)
loglevel = "info"
