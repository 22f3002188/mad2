# celery_app.py
from celery import Celery
from celery.schedules import schedule

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0',
        include=['tasks']  # ✅ auto-import tasks.py
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'send-test-email-every-30s': {
            'task': 'tasks.send_daily_reminders',
            'schedule': schedule(30.0),
        },
        'send-monthly-report-every-30s': {
            'task': 'tasks.send_monthly_report',
            'schedule': schedule(30.0),
        }
    }

    return celery
