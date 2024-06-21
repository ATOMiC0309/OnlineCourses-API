# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import (Profile, Lesson, Section, LessonVideo, Comment, ReplyToComment, Course, UserNotification)
from .serializers import (ProfileSerializer, LessonSerializer, LessonVideoSerializer, CommentSerializer,
                          ReplyToCommentSerializer, CourseSerializer, SectionSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.order_by('-pk')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class CourseAPIViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.order_by('-pk')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class SectionAPIViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.order_by('-pk')
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.order_by('-pk')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        lesson = self.get_object()
        lesson.like(request.user)
        serializer = self.get_serializer(lesson)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        lesson = self.get_object()
        lesson.dislike(request.user)
        serializer = self.get_serializer(lesson)
        return Response(serializer.data)


class LessonVideoViewSet(viewsets.ModelViewSet):
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-pk')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReplyToCommentViewSet(viewsets.ModelViewSet):
    queryset = ReplyToComment.objects.order_by('-pk')
    serializer_class = ReplyToCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
def search_lessons(request):
    query = request.query_params.get('query', '')

    lessons = Lesson.objects.filter(Q(topic__icontains=query) | Q(description__icontains=query))

    serialized_lessons = LessonSerializer(lessons, many=True)
    return Response(serialized_lessons.data)


@api_view(['POST'])
def send_email_to_users(request):
    subject = request.data.get('subject', '')
    message = request.data.get('message', '')

    if not subject or not message:
        return Response({'error': 'Subject and message are required.'}, status=400)

    users = User.objects.all()
    rec_emails = ""
    UserNotification.objects.create(subject=subject, message=message)

    for user in users:
        send_mail(
            subject,
            message,
            'sender@example.com',
            [user.email],
            fail_silently=False,
        )
        rec_emails += user.email + ", "

    return Response({'success': f'Emails {rec_emails} sent successfully.'}, status=200)

