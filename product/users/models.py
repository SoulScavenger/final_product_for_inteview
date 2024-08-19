from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Group


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user_balance = models.PositiveBigIntegerField(default=1000)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='ИД пользователя'
    )

    course_id = models.PositiveIntegerField(
        verbose_name="ИД курса"
    )

    course_title = models.CharField(
        max_length=250,
        verbose_name='Название курса',
    )

    has_subscription = models.BooleanField(default=False,
                                           verbose_name='Подписка')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

