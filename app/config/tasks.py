from typing import List
from celery import shared_task
from app.services.post_requests import fire_and_forget, post_request
from app.core.config import get_app_settings
from app.models.domain.tasks import TaskStatus

SETTINGS = get_app_settings()

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 50},
             name='tasks:generate_avatars_task')
def post_to_generate_avatars_api(self, body, task_list_count):  
       if task_list_count <= SETTINGS.total_ds_replicas:
           post_request(SETTINGS.ds_api_url, body=body, request_type="POST") 
       else:
            self.retry(countdown = SETTINGS.celery_worker_wait_time)