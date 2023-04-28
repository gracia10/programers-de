from django.test import TestCase
from polls_api.serializers import *


class VoteSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='1'
        )

    def test_vote_serializer(self):
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()

        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)

    def test_vote_serializer_with_duplicate_vote(self):
        self.assertEqual(User.objects.all().count(), 1)
        choice1 = Choice.objects.create(
            question=self.question,
            choice_text='2'
        )
        Vote.objects.create(question=self.question, choice=choice1, voter=self.user)

        data = {
            'question': self.question.id,
            'choice': choice1.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_vote_serilaizer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )

        choice2 = Choice.objects.create(
            question=question2,
            choice_text='1'
        )
        data = {
            'question': self.question.id,
            'choice': self.choice.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())


def test_vote_serializer(self):
    user = User.objects.create(username="testuser")
    question = Question.objects.create(question_text="abc", owner=user)
    choice = Choice.objects.create(choice_text="a", question=question)

    data = {'voter': user.id, 'question': question.id, 'choice': choice.id}
    serializer = VoteSerializer(data=data)
    self.assertTrue(serializer.is_valid())
    vote = serializer.save()

    self.assertEqual(vote.question, question)
    self.assertEqual(vote.choice, choice)
    self.assertEqual(vote.voter, user)


class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data={'question_text': 'abc'})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={'question_text': ''})
        self.assertEqual(serializer.is_valid(), False)
