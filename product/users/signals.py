from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Course
from .models import Balance, CustomUser, Subscription


@receiver(post_save, sender=CustomUser)
def post_updata_subscription(sender, instance: CustomUser, created, **kwargs):
    """Заполнение таблиц Подписки и Баланса при создании пользователя."""
    if created:
        courses_id = Course.objects.values('id')
        if len(courses_id):
            for course_id in courses_id:
                Subscription.objects.create(
                    user_id=instance.id,
                    course_id=course_id.get('id'),
                    course_title=course_id.get('title')
                    )

@receiver(post_save, sender=CustomUser)
def post_update_balance(sender, instance: CustomUser, created, **kwargs):
    """Заполнение таблицы Баланс при создании пользователя."""
    if created:
        Balance.objects.create(user_id=instance.id, user_balance=1000)