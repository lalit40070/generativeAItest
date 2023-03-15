import os
from functools import lru_cache
from kombu import Queue
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = SETTINGS.celery_broker_url
    CELERY_RESULT_BACKEND: str = SETTINGS.celery_result_backend

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # custom queue
        Queue("tasks"),
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    pass


""" Not needed. Remove it """
@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = "development"
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()