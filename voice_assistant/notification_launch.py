import configparser
import time

from src.win10toast.win10toast import ToastNotifier
from app import *

config = configparser.ConfigParser()
config.read("config.ini")
delay = int(config.get("notifications", "notifications_delay"))
duration = int(config.get("notifications", "notifications_duration"))


toast = ToastNotifier()
while True:
    time.sleep(delay)
    toast.show_toast('Job Assistant', 'Доступна новая вакансия', duration=duration, threaded=True, callback_on_click=main)
