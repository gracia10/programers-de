from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from polls.models import Question
from polls_api.serializers import QuestionSerializer


@api_view(['GET', 'POST'])
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def question_detail(request, id):
    questions = get_object_or_404(pk=id)

    if request.method == 'GET':
        serializer = QuestionSerializer(questions)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = QuestionSerializer(questions)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
