from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    """This model is for user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile-images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "1. Profile"


class BaseModel(models.Model):
    """This model is designed to avoid overwriting common fields"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    """This model is for courses"""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    for_whom = models.TextField()
    teacher_fullname = models.CharField(max_length=150, help_text="The full name of the person teaching this course.")
    teacher_picture = models.ImageField(upload_to='teachers/',
                                        help_text="A picture of the person teaching this course.")
    about_teacher = models.TextField(help_text="Information about the person teaching this course "
                                               "(experience, knowledge, portfolio...)")
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "2. Courses"


class Section(BaseModel):
    """This model is designed to divide the lessons in the course into sections"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course}: {self.title}"

    class Meta:
        verbose_name_plural = "3. Sections"


class Lesson(BaseModel):
    """This model is intended for lessons in the course"""
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                help_text="What section of the course does the lesson belong to?")
    topic = models.CharField(max_length=250, help_text="Lesson topic.")
    description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='lesson_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='lesson_dislikes', blank=True)

    def __str__(self):
        return (f"{self.section.course}\n"
                f"{self.section}: {self.topic}")

    def like(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
            if user in self.dislikes.all():
                self.dislikes.remove(user)

    def dislike(self, user):
        if user not in self.dislikes.all():
            self.dislikes.add(user)
            if user in self.likes.all():
                self.likes.remove(user)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()

    class Meta:
        verbose_name_plural = "4. Lessons"


class LessonVideo(BaseModel):
    """This model is for videos in class"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    video_content = models.FileField(upload_to='lesson-videos/',
                                     validators=[
                                         FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])],
                                     help_text="Upload videos in *.mp4, *.mov, *.avi and *.mkv formats for this lesson!")

    class Meta:
        verbose_name_plural = "5. Lesson Videos"


class Comment(BaseModel):
    """This model is for commenting on the lesson"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.author.username}: {self.message}"


class ReplyToComment(BaseModel):
    """This model is for writing a response to a comment left in the lesson"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.author.username}: {self.message}"


class UserNotification(models.Model):
    """This model is for messages sent to users"""
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "7. Messages sent to users"


class UserStartedCourse(models.Model):
    """This model is designed for user-initiated courses"""
    course = models.ManyToManyField(Course)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}: {self.course} // {self.started}"

    class Meta:
        verbose_name_plural = "6. Courses initiated by the user"
