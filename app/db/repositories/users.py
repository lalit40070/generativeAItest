from typing import Optional
from datetime import datetime


from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import User, UserInDB, SocialAuthType
from app.models.domain.images import ImageType
from app.models.domain.tasks import TaskStatus
from app.models.schemas.users import (
                    UserPackInResponse, 
                    UserPacksInResponse, 
                    UserPackImageResultsRows,
                    UserPackProcessingInReponse,
                    UserPacksBriefInResponse) 
from app.services.s3_fetch_all_images import get_all_images
from app.services.s3_connector import s3_connector
from app.services.s3_generate_presigned_urls import gen_pre_signed_url_from_key, gen_cloud_front_url_from_key
from app.core.config import get_app_settings
from app.services.image_banner_generator import create_banner
from app.models.domain.tasks import Task

SETTINGS = get_app_settings()


class UsersRepository(BaseRepository):
    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_row = await queries.get_user_by_email(self.connection, email=email)
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist("user with email {0} does not exist".format(email))

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await queries.get_user_by_username(
            self.connection,
            username=username,
        )
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(
            "user with username {0} does not exist".format(username),
        )
    
    async def get_user_by_id(self, *, user_id: int) -> UserInDB:
        user_row = await queries.get_user_by_user_id(
            self.connection,
            id=user_id,
        )
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(
            "user with user_id {0} does not exist".format(user_id),
        )


    async def get_user_by_identifier(self, *, user_identifier: str) -> UserInDB:
        user_row = await queries.get_user_by_user_identifier(
            self.connection,
            user_identifier=user_identifier,
        )
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(
            "user with user_identifier {0} does not exist".format(user_identifier),
        )

    async def delete_user(self, user_identifier:str):
        async with self.connection.transaction():
            await queries.delete_user(
                self.connection,
                identifier=user_identifier,
                is_active=False
            )

    async def get_user_by_apple_id(self, *, id_for_apple: int) -> UserInDB:
        user_row = await queries.get_user_by_apple_id(
            self.connection,
            id_for_apple=id_for_apple,
        )
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(
            "user with apple_id {0} does not exist".format(id_for_apple),
        )
    async def get_image_signed_urls(self, url, s3_connector_obj):
        images = get_all_images(s3_connector_obj, ImageType.AVATAR.toString(),url)
        return [gen_cloud_front_url_from_key(image) for image in images]

    async def get_user_packs(self, user_identifier:str) -> list[UserPacksInResponse]:
        task_rows = await self.connection.fetch("select * from tasks where user_identifier = '{}'".format(user_identifier))
        processed_task_rows = [task_row for task_row in task_rows if task_row["task_status"]==TaskStatus.SUCCESS.toString()]
        unprocessed_task_rows = list(set(task_rows)- set(processed_task_rows))
        tasks_list_in_reponse: list[UserPackInResponse] = []
        s3_connector_obj = s3_connector()

        for unprocessed_task in unprocessed_task_rows:
            image_rows = []
            pack_row = await queries.get_pack_details(
                            self.connection,
                            pack_id=unprocessed_task["pack_id"])

            pack_id = pack_row["pack_name"]
            images_per_pack = pack_row["images_per_pack"]
            task_status = unprocessed_task["task_status"]
            timezone_info = unprocessed_task["created_at"].tzinfo
            banner_image = ""
            task_id = unprocessed_task["id"]
            time_left_absolute = SETTINGS.processing_time - ((datetime.now(timezone_info) - unprocessed_task["created_at"]).total_seconds())
            time_left = time_left_absolute if time_left_absolute > 0 else 300
            single_task_in_reponse = UserPacksBriefInResponse( 
                                                                pack_id=pack_id,
                                                                task_status = task_status,
                                                                images_per_pack = images_per_pack,
                                                                time_left= time_left,
                                                                banner_image=banner_image,
                                                                task_id=task_id
                                                                )
            tasks_list_in_reponse.append(single_task_in_reponse)

        for processed_task in processed_task_rows:
 
            """" move this to query files post fixing multiple row fetching"""
            query_string = """select url, style from images where user_identifier= '{}' 
                            and purchase_id = '{}' and type = '{}'""".format(user_identifier,
                                                                         processed_task["purchase_id"],
                                                                         ImageType.AVATAR.toString())
                                                    
            image_rows = await self.connection.fetch(query_string)
            pack_row = await queries.get_pack_details(
                            self.connection,
                            pack_id=processed_task["pack_id"])

            pack_id = pack_row["pack_name"]
            images_per_pack = pack_row["images_per_pack"]
            task_status = processed_task["task_status"]
            task_id = processed_task["id"]

            banner_image = create_banner(s3_connector_obj, images=[image_row['url'] for image_row in image_rows[:3]] , 
                            purchase=processed_task["purchase_id"], 
                            user=user_identifier)
            
            single_task_in_reponse = UserPacksBriefInResponse(
                                                                pack_id=pack_id,
                                                                task_status = task_status,
                                                                images_per_pack =images_per_pack,
                                                                time_left=0,
                                                                banner_image=banner_image,
                                                                task_id = task_id
                                                                )
            tasks_list_in_reponse.append(single_task_in_reponse)

        return tasks_list_in_reponse

    
    async def get_user_packs_by_task_id(self, user_identifier:str, task:Task) -> UserPacksInResponse:
        style_names = await self.connection.fetch("select * from style")
        style_names_dict = dict([(row["style_id"], row["name"]) for row in style_names])
       
        s3_connector_obj = s3_connector()
        if task.status == TaskStatus.SUCCESS.toString():

            """" move this to query files post fixing multiple row fetching"""
            query_string = """select url, style from images where user_identifier= '{}' 
                            and purchase_id = '{}' and type = '{}'""".format(user_identifier,
                                                                         task.purchase_id.purchase_id,
                                                                         ImageType.AVATAR.toString())
                                                    
            image_rows = await self.connection.fetch(query_string)
            image_rows_for_output = [UserPackImageResultsRows(
                                images_url = await self.get_image_signed_urls(image_row['url'], s3_connector_obj),
                                style_name= style_names_dict[image_row["style"]]) 
                                for image_row in image_rows]
            pack_row = await queries.get_pack_details(
                            self.connection,
                            pack_id=task.pack_id.pack_id)

            pack_id = pack_row["pack_name"]
            images_per_pack = pack_row["images_per_pack"]

            banner_image = create_banner(s3_connector_obj, images=[image_row['url'] for image_row in image_rows[:3]] , 
                            purchase=task.purchase_id.purchase_id, 
                            user=user_identifier)
            task_id = task.task_id
            single_task_in_reponse = UserPackInResponse(image_rows=image_rows_for_output, 
                                                                pack_id=pack_id,
                                                                task_status = task.status,
                                                                images_per_pack =images_per_pack,
                                                                time_left=0,
                                                                banner_image=banner_image,
                                                                task_id = task_id
                                                                )
            return single_task_in_reponse

        else:
            image_rows = []
            image_rows_for_output = [UserPackImageResultsRows(
                                images_url = self.get_image_signed_urls(image_row['url'], s3_connector_obj),
                                style_name= style_names_dict[image_row["style"]]) 
                                for image_row in image_rows]
            pack_row = await queries.get_pack_details(
                            self.connection,
                            pack_id=task.pack_id.pack_id)

            pack_id = pack_row["pack_name"]
            images_per_pack = pack_row["images_per_pack"]
            task_status = task.status
            timezone_info = task.created_at.tzinfo
            banner_image = ""
            task_id = task.task_id
            time_left_absolute = SETTINGS.processing_time - ((datetime.now(timezone_info) - task.created_at).total_seconds())
            time_left = time_left_absolute if time_left_absolute > 0 else 300
            single_task_in_reponse = UserPackProcessingInReponse(image_rows=image_rows_for_output, 
                                                                pack_id=pack_id,
                                                                task_status = task_status,
                                                                images_per_pack = images_per_pack,
                                                                time_left= time_left,
                                                                banner_image=banner_image,
                                                                task_id=task_id
                                                                )

        
            return single_task_in_reponse 


    
     
    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
        device_id: Optional[str] = None,
        fcm_token: Optional[str] = None,
        is_subscribed: bool,
        auth_type: SocialAuthType,
        identifier: str,
        id_for_apple:str
    ) -> UserInDB:
        user = UserInDB(username=username, email=email, device_id=device_id, 
                        fcm_token=fcm_token, id_for_apple=id_for_apple,
                        is_subscribed=is_subscribed,auth_type=auth_type, identifier=identifier)
        user.change_password(password)

        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection,
                username=user.username,
                identifier=user.identifier,
                email=user.email,
                salt=user.salt,
                hashed_password=user.hashed_password,
                device_id=user.device_id,
                fcm_token=user.fcm_token,
                is_subscribed=user.is_subscribed,
                auth_type=user.auth_type,
                id_for_apple=user.id_for_apple
            )
        
        async with self.connection.transaction():
            notification_row = await queries.create_notification(
                self.connection,
                is_allowed = False, 
                user_id = user.identifier

            )
        
        user_row_updated = {k: v if v is not None else 'None' for k, v in user_row.items()}

        return user.copy(update=dict(user_row_updated))

    async def update_user(  # noqa: WPS211
        self,
        *,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        device_id:Optional[str] = None,
        fcm_token:Optional[str] = None,
        is_subscribed:Optional[bool] = False,
        auth_type: SocialAuthType
    ) -> UserInDB:
        user_in_db = await self.get_user_by_username(username=user.username)

        user_in_db.username = user_in_db.username or username  
        user_in_db.email = user_in_db.email or email
        user_in_db.device_id = user_in_db.device_id or device_id  
        user_in_db.fcm_token = user_in_db.fcm_token or fcm_token 
        user_in_db.is_subscribed = user_in_db.is_subscribed or is_subscribed 
        user_in_db.auth_type = user_in_db.auth_type or auth_type  
        if password:
            user_in_db.change_password(password)

        async with self.connection.transaction():
            user_in_db.updated_at = await queries.update_user_by_username(
                self.connection,
                username=user.username,
                new_username=user_in_db.username,
                new_email=user_in_db.email,
                new_salt=user_in_db.salt,
                new_password=user_in_db.hashed_password,
                new_device_id=user_in_db.device_id,
                new_fcm_token=user_in_db.fcm_token,
                new_is_subscribed=user_in_db.is_subscribed,
                new_auth_type=user_in_db.auth_type,
            )

        return user_in_db


