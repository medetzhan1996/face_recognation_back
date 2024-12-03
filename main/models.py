import uuid
import os

from django.db import models


def generate_unique_file_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4()}{extension}"
    return os.path.join('client_photos', unique_filename)


class Client(models.Model):
    name = models.CharField("Имя", max_length=100)
    photo = models.ImageField("Фото", upload_to=generate_unique_file_path)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
