from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import (Course, Section, Lesson, LessonVideo, Profile, Comment, ReplyToComment,
                     UserNotification, UserStartedCourse)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """This is to display the class profile model in the admin panel"""
    list_display = ('pk', 'user', 'bio', 'location', 'get_pic')
    list_display_links = ('pk', 'user')

    def get_pic(self, profile):
        if profile.picture:
            url = profile.picture.url
        else:
            url = "https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o="
        return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" alt="no image" width="60px"></a>')

    get_pic.short_description = "Profile picture."


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """This is to display the class course model in the admin panel"""
    list_display = ('pk', 'name', 'for_whom', 'price', 'teacher_fullname', 'get_pic')
    list_display_links = ('pk', 'name')

    def get_pic(self, course):
        if course.teacher_picture:
            url = course.teacher_picture.url
        else:
            url = "https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o="
        return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" alt="no image" width="60px"></a>')

    get_pic.short_description = "Teacher picture"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """This is to display the class section model in the admin panel"""
    list_display = ("pk", "course", "title", "description")
    list_display_links = ("pk", "title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """This is to display the class lesson model in the admin panel"""
    list_display = ('pk', 'section', 'topic', 'description', 'total_likes', 'total_dislikes')
    list_display_links = ('pk', 'topic')


@admin.register(LessonVideo)
class LessonVideoAdmin(admin.ModelAdmin):
    """This is to display the class LessonVideo model in the admin panel"""
    list_display = ('pk', 'lesson', 'video_content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """This is to display the class comment model in the admin panel"""
    list_display = ('pk', 'lesson', 'message', 'author')


@admin.register(ReplyToComment)
class ReplyToCommentAdmin(admin.ModelAdmin):
    """This is to display the class ReplyToComment model in the admin panel"""
    list_display = ('pk', 'comment', 'message', 'author')


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    """This is to display the class UserNotification model in the admin panel"""
    list_display = ('pk', 'subject', 'message', 'created')


@admin.register(UserStartedCourse)
class UserStartedCourseAdmin(admin.ModelAdmin):
    """This is to display the class UserStartedCourse model in the admin panel"""
    list_display = ('pk', 'get_courses', 'student', 'started')

    def get_courses(self, obj):
        return ", ".join([c.name for c in obj.course.all()])

    get_courses.short_description = 'Courses'
