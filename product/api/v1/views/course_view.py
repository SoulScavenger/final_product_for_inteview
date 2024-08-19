from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin, make_payment
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group, Lesson
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)
    
    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        queryset = Lesson.objects.select_related('course').all().filter(
            course_id=course)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        queryset = Group.objects.select_related('course').all().filter(
            course_id=course)
        return queryset


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['post', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post', ],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        course_info = self.get_object()
        user_info = Subscription.objects.get(user_id=request.user.id,
                                             course_id=pk)
        course_price = course_info.price
        if not course_info.is_available:
            return Response(
                {"info": "Курс не доступен"}, 
                status=status.HTTP_418_IM_A_TEAPOT)
        elif user_info.has_subscription:
            return Response(
                {"info": "Курс уже приобретен"}, 
                status=status.HTTP_418_IM_A_TEAPOT)
        elif make_payment(request=request, course_price=course_price):
            user_info.has_subscription = True
            user_info.save()
        else:
            return Response(
                {"info": "Недостаточно средств"}, 
                status=status.HTTP_418_IM_A_TEAPOT)

        serializer = SubscriptionSerializer(instance=user_info)
        data = serializer.data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
