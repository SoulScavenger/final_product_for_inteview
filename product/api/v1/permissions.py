from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription, Balance




def make_payment(request, course_price):
    balance = Balance.objects.select_related('user').get(
        user_id=request.user.id
        )
    if balance.user_balance >= course_price:
        balance.user_balance -= course_price
        balance.save()
        return True
    else:
        return False



class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        has_user_access = Subscription.objects.get(
            user_id=request.user.id,
            course_id=view.kwargs.get('course_id')
            ).has_subscription

        return (request.user.is_superuser
                or request.user.is_staff
                or (has_user_access
                    and request.method in SAFE_METHODS))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.is_staff
                or request.method in SAFE_METHODS)


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
