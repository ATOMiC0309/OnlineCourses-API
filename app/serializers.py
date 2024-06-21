from rest_framework import serializers
from .models import Profile, Lesson, LessonVideo, Comment, ReplyToComment, Section, Course, UserNotification
from django.contrib.auth.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'birth_date', 'picture']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UsersSerializer.create(UsersSerializer(), validated_data=user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if 'password' in user_data:
            user.set_password(user_data['password'])
        user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance


class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'lesson', 'message', 'author', 'created', 'updated']


class ReplyToCommentSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)

    class Meta:
        model = ReplyToComment
        fields = ['id', 'comment', 'message', 'author', 'created', 'updated']


class LessonSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'section', 'topic', 'description', 'likes', 'dislikes', 'total_likes', 'total_dislikes',
                  'created', 'updated']


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'user', 'subject', 'message', 'created']
