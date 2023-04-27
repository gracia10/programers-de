from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from polls.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner']


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'questions']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # override
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "not same"})
        return attrs

    # 모델에는 없는 password2 필드 때문에 create를 오버라이드한다
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
