from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseAPIViewSet, LessonViewSet, SectionAPIViewSet, LessonVideoViewSet, CommentViewSet,
                    ReplyToCommentViewSet, ProfileViewSet, search_lessons, send_email_to_users)

routers = DefaultRouter()
routers.register('courses', CourseAPIViewSet, basename='courses')
routers.register('sections', SectionAPIViewSet, basename='sections')
routers.register('lessons', LessonViewSet, basename='lessons')
routers.register('lesson-videos', LessonVideoViewSet, basename='lesson-videos')
routers.register('comments', CommentViewSet, basename='comments')
routers.register('reply-to-comments', ReplyToCommentViewSet, basename='reply-to-comments')
routers.register('profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path('online-courses-api/', include(routers.urls)),
    path('online-courses-api/lessons-search/', search_lessons),
    path('online-courses-api/send-mail/', send_email_to_users),
]
