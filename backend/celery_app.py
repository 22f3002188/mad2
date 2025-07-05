# celery_app.py
from celery import Celery
from celery.schedules import crontab
from celery.schedules import schedule
# import tasks

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'send-daily-reminders': {
            'task': 'tasks.send_daily_reminders',
            'schedule': crontab(hour=18, minute=0),  # 6 PM daily
        },
        'send-monthly-report': {
            'task': 'tasks.send_monthly_report',
            'schedule': crontab(minute=0, hour=6, day_of_month=1),  # 6 AM on 1st of each month
        }
    }    
    
    # celery.conf.beat_schedule = {
    #     'send-test-email-every-30s': {
    #         'task': 'tasks.send_daily_reminders',
    #         'schedule': schedule(30.0),  # Every 30 seconds
    #     },
    #     'send-monthly-report-every-30s': {
    #         'task': 'tasks.send_monthly_report',
    #         'schedule': schedule(30.0),  # Every 30 seconds
    #     }
    # }
      


    return celery
