from patio import Registry, AsyncExecutor
from patio_rabbitmq import RabbitMQBroker
from src.settings import get_settings

settings = get_settings()

broker : RabbitMQBroker | None = None
executor : AsyncExecutor | None = None
rpc = Registry(project=settings.broker_project_name, auto_naming=False)