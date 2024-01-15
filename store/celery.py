import os
from kombu import Exchange, Queue
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
app = Celery('store')

# Явное указание брокера (RabbitMQ)
app.conf.broker_url = 'pyamqp://admin:zGstiw3259!@127.0.0.1:5672'

# Использование настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

# Дополнительные конфигурации Celery...

# Определение очередей (если нужно)
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    # Добавьте больше очередей, если это необходимо...
)
