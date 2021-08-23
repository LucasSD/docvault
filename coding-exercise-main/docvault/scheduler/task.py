import os

from django.contrib.auth.models import User
from django.core.mail import send_mail as sm
from docvault.scheduler.celery import app

from celery.schedules import crontab


@app.task(name="mod", bind=True, default_retry_delay=10, max_retries=5)
def mod(self, x, y):
    try:
        z = x % y
        print(f'{x} % {y} = {x%y}')
        return z
    except :
        mod.retry()
        print(f'Error with mod')



app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}

@app.task(name="send_notification", bind=True, default_retry_delay=300, max_retries=5)
def send_notification(self, subject, message):
    

    # Fetch all users except superuser
    users = User.objects.exclude(is_superuser=True).all()
    user_emails = [user.email for user in users]
    num_users = len(user_emails)

    # try sending email
    try:
        res = sm(
            subject=subject,
            html_message=message,
            from_email=os.environ.get("EMAIL_HOST_USER"),
            recipient_list=user_emails,
            fail_silently=False,
            message=None)
        print(f'Email sent to {len(user_emails)} users')
    except Exception:

        # retry when fail
        send_notification.retry()
