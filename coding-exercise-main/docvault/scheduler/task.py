from docvault.scheduler.celery import app

@app.task(name="mod", bind=True, default_retry_delay=10, max_retries=5)
def mod(self, x, y):
    try:
        z = x % y
        print(f'{x} % {y} = {x%y}')
        return z
    except :
        mod.retry()
        print(f'Error with mod')