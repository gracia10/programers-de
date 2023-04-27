from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': '선택이 없습니다'})

    selected_choice.votes = F('votes') + 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


class SingleView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user-list')
    template_name = 'registration/signup.html'
