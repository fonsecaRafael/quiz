from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def question(request, id):
    context = {'id_question': id}
    return render(request, 'base/game.html', context=context)


def ranking(request):
    return render(request, 'base/end.html')
