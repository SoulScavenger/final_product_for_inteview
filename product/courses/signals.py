from django.db.models import Count, Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import Subscription, CustomUser
from .models import Course, Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """
    if not created:
        next_group = 1
        group_info = Group.objects.all().filter(course_id=instance.course_id)
        print(group_info)
        if len(group_info):
            group_info = group_info.latest('id')
            last_grup_number = group_info.number
            if last_grup_number <= 9:
                next_group += last_grup_number

        Group.objects.create(
            number=next_group,
            title=f"Группа {next_group}. {instance.course_title}",
            course_id=instance.course_id,
            user_id=instance.user_id
        )


@receiver(post_save, sender=Course)
def post_updata_subscription(sender, instance: Course, created, **kwargs):
    """Заполнение таблицы Подписки при создании курса."""
    if created:
        users_id = CustomUser.objects.values('id')
        if len(users_id) > 0:
            for user_id in users_id:
                Subscription.objects.create(
                    user_id=user_id.get('id'),
                    course_id=instance.id,
                    course_title=instance.title)

