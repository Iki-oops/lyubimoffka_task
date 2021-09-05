from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


User = get_user_model()


class Company(models.Model):
    address = models.CharField(max_length=128, verbose_name='Адрес')
    name = models.CharField(max_length=128, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')

    class Meta:
        verbose_name_plural = 'Компании'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Employee(models.Model):
    full_name = models.CharField(verbose_name='ФИО', max_length=128)
    position = models.CharField(verbose_name='Должность', max_length=128)
    phone_regex = RegexValidator(regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
                                 message='Incorrect phone number.')
    work = models.CharField(validators=[phone_regex], max_length=20,
                            verbose_name='Рабочий', help_text='Обязателен к заполнению', default='')
    private = models.CharField(validators=[phone_regex], max_length=20, verbose_name='Личный',
                               null=True, blank=True, unique=True)
    fax = models.CharField(validators=[phone_regex], max_length=20, verbose_name='Факс',
                           null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')

    class Meta:
        verbose_name_plural = 'Работники'
        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'company'],
                name='unique_name_in_company'
            )
        ]

    def __str__(self):
        return self.full_name
