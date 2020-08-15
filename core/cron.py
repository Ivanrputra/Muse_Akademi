# myapp/cron.py
import cronjobs

@cronjobs.register
def periodic_task():
    print('asdadasd')