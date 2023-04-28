from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote


class VoteSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['choice'].question.id != attrs['question'].id:
            raise serializers.ValidationError("incorrect answer")
        return attrs

    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['question', 'voter']
            )
        ]


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    def get_votes_count(self, obj):
        return obj.vote_set.count()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail')

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
