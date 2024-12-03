import boto3
from botocore.exceptions import ClientError
import os


AWS_REGION = "ap-south-1"
AWS_PROFILE = "default"

def get_client(service):
    """Возвращает клиент для указанной службы AWS."""
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        return session.client(service, region_name=AWS_REGION)
    except Exception as e:
        raise

def create_collection(collection_id):
    """Создаёт коллекцию Rekognition."""
    client = get_client('rekognition')
    try:
        response = client.create_collection(CollectionId=collection_id)
        return {
            "CollectionArn": response["CollectionArn"],
            "StatusCode": response["StatusCode"]
        }
    except ClientError as e:
        raise

def list_collections():
    """Выводит список существующих коллекций."""
    client = get_client('rekognition')
    try:
        response = client.list_collections(MaxResults=10)
        return response.get('CollectionIds', [])
    except ClientError as e:
        raise

def delete_user(collection_id, user_id):
    """Удаляет пользователя из коллекции."""
    client = get_client('rekognition')
    try:
        client.delete_user(CollectionId=collection_id, UserId=user_id)
        return {"UserId": user_id, "Status": "Deleted"}
    except ClientError as e:
        pass

def upload_file_to_s3(bucket_name, file_name, object_name=None):
    """Загружает файл в указанный бакет S3."""
    s3 = get_client('s3')
    if object_name is None:
        object_name = file_name
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        return {"BucketName": bucket_name, "ObjectName": object_name}
    except Exception as e:
        raise

def add_faces_to_collection(bucket, photo, collection_id):
    """Добавляет лицо из изображения в коллекцию Rekognition."""
    client = get_client('rekognition')
    try:
        response = client.index_faces(
            CollectionId=collection_id,
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            ExternalImageId=photo,
            MaxFaces=1,
            QualityFilter="AUTO",
            DetectionAttributes=['ALL']
        )
        face_ids = [face['Face']['FaceId'] for face in response.get('FaceRecords', [])]
        return {"FaceIds": face_ids, "UnindexedFaces": response.get('UnindexedFaces', [])}
    except ClientError as e:
        raise

def create_user(collection_id, user_id):
    """Создаёт пользователя в коллекции."""
    client = get_client('rekognition')
    try:
        client.create_user(CollectionId=collection_id, UserId=user_id)
        return {"UserId": user_id, "CollectionId": collection_id, "Status": "Created"}
    except ClientError as e:
        raise

def associate_faces(collection_id, user_id, face_ids):
    """Привязывает лица к пользователю."""
    client = get_client('rekognition')
    try:
        response = client.associate_faces(CollectionId=collection_id, UserId=user_id, FaceIds=face_ids)
        return {"AssociatedFaces": response.get("AssociatedFaces", []), "UnsuccessfulFaceAssociations": response.get("UnsuccessfulFaceAssociations", [])}
    except ClientError as e:
        raise

def search_users_by_image(collection_id, image_bytes):
    """Ищет пользователя по изображению."""
    client = get_client('rekognition')
    try:
        response = client.search_users_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes}
        )
        matches = [
            {"UserId": match["User"]["UserId"], "Similarity": match["Similarity"]}
            for match in response.get("UserMatches", [])
        ]
        return {"Matches": matches}
    except ClientError as e:
        raise

def main():
    # Конфигурация
    collection_id = "kgdemo_collection"
    bucket_name = "kgdemobucket"
    photo = "medet.jpg"
    user_id = "2"

    # Проверка существования локального файла
    if not os.path.exists(photo):
        print(f"Файл {photo} не найден.")
        return

    try:
        # 1. Список коллекций
        #list_collections()

        # 2. Создание коллекции
        # create_collection(collection_id)

        # 3. Загрузка изображения в S3
        # upload_file_to_s3(bucket_name, photo)

        # 4. Добавление лица в коллекцию
        # face_ids = add_faces_to_collection(bucket_name, photo, collection_id)

        # 5. Создание пользователя
        # create_user(collection_id, user_id)

        # 6. Привязка лица к пользователю
        # associate_faces(collection_id, user_id, face_ids.get("FaceIds"))

        # 7. Поиск пользователя по изображению
        print(search_users_by_image(collection_id, photo))

    except Exception as e:
        print(f"Ошибка выполнения: {e}")