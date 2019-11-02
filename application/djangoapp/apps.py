import datetime

import os

from django.apps import AppConfig
from apipkg import api_manager as api
from datetime import datetime, timedelta

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])

            if 'ENV' in os.environ:
                if os.environ['ENV'] == 'dev':
                    api.post_request(host='scheduler', url='/app/delete?source=caisse', body={})

            from .views import schedule_task

            clock_time = api.send_request('scheduler', 'clock/time')
            time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
            time = time + timedelta(minutes=15)
            schedule_task("caisse", "/database_update_scheduled", time, "day", "", "caisse", "Caisse: Update Products")
