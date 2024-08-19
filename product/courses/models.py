from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Название курса',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    price = models.PositiveIntegerField(
        verbose_name="Цена"
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name='В наличии')
        
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название урока',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс"
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    number = models.PositiveBigIntegerField(
        verbose_name="Номер группы"
    )

    title = models.CharField(
        max_length=250,
        verbose_name='Название группы'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )

    user_id = models.PositiveIntegerField(
        default=0,
        verbose_name='ИД студента'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
