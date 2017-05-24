from .celery import *
import os

# To use celery in memory
#task_always_eager = True

broker_url = 'amqp://guest:guest@rabbit:5672//'
if os.getenv('TAIGA_BROKER_URL') is not None:
    broker_url = os.getenv('TAIGA_BROKER_URL')

result_backend = 'redis://redis:6379/0'
if os.getenv('TAIGA_RESULT_BACKEND') is not None:
    result_backend = os.getenv('TAIGA_RESULT_BACKEND')
