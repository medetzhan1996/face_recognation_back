import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Client
from .recognaton_service import (
    upload_file_to_s3,
    add_faces_to_collection,
    create_user,
    associate_faces, delete_user,
)


@receiver(post_save, sender=Client)
def after_client_created(sender, instance, created, **kwargs):
    if created:
        collection_id = "kgdemo_collection"
        bucket_name = "kgdemobucket"
        user_id = str(instance.id)
        photo_path = instance.photo.name
        photo_obj = instance.photo.path
        photo = os.path.basename(photo_path)
        upload_file_to_s3(bucket_name, photo_obj, photo)
        face_ids = add_faces_to_collection(bucket_name, photo, collection_id)
        create_user(collection_id, user_id)
        associate_faces(collection_id, user_id, face_ids.get("FaceIds"))


@receiver(post_delete, sender=Client)
def after_client_deleted(sender, instance, **kwargs):
    collection_id = "kgdemo_collection"
    user_id = str(instance.id)
    delete_user(collection_id, user_id)