from datetime import timezone

from polls_api.permissions import *
from polls_api.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {'question_text': 'some question'}
        self.url = reverse('queston-list')

    def test_create_question(self):
        user = User.objects.create(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.question_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertEqual((timezone.now - question.pub_date).total_seconds(), 1)

    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_question(self):
        question = Question.objects.create(question_text='Question1')
        choice = Choice.objects.create(question=question, choice_text='Question1')
        Question.objects.create(question_text='Question2')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# 유저의 투표 내역
class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # mixin create 함수는 validate 후 votor의 정보를 받아 not found error 발생
        # voter 정보를 serializer에게 제공한 뒤 작업하도록 수정
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    # votor가 변경되지 않도록 오버라이딩
    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)
