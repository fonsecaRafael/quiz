from django.shortcuts import render
from base.models import Question


def home(request):
    return render(request, 'base/home.html')


def question(request, id):
    question = Question.objects.filter(enable=True).order_by('id')[id - 1]
    context = {'question': question}
    return render(request, 'base/game.html', context)


def ranking(request):
    return render(request, 'base/end.html')
