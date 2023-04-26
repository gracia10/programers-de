from rest_framework import serializers

from polls.models import Question


class QuestionSerializer(serializers.Serializer):
    # 직렬화 필드
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)

    # 인스턴스 생성
    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    # 인스턴스 필드 수정
    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.save()
        return instance
