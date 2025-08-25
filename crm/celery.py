from celery import Celery

redis_url = 'redis://localhost:6379/0'
celery_app = Celery('crm', broker=redis_url)
