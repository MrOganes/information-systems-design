from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email', unique=True)
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True, null=True)
    address = models.CharField(max_length=500, verbose_name='Адрес', blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=100, blank=True, null=True)
    postal_code = models.CharField(verbose_name='Почтовый индекс', max_length=20, blank=True, null=True)
    country = models.CharField(verbose_name='Страна', max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    class Meta:
        app_label = 'cabinet'
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
