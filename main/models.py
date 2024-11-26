from django.db import models



class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    last_name = models.CharField("Фамилия", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    second_name = models.CharField("Отчество", max_length=50, blank=True, null=True)
    id_document = models.CharField("Идентификатор удостоверения личности", max_length=100, unique=True)
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)
    address = models.TextField("Адрес")
    workplace = models.CharField("Место работы", max_length=100, blank=True, null=True)
    photo = models.ImageField("Фотография", upload_to='client_photos/')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name or ''}".strip()

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
