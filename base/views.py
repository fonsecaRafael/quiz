from django.shortcuts import render, redirect
from base.models import Question, Player
from base.forms import PlayerForm


def home(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            player = Player.objects.get(email=email)
        except Player.DoesNotExist:
            form = PlayerForm(request.POST)
            if form.is_valid():
                player = form.save()
                request.session['player_id'] = player.id
                return redirect('/question/1')
            else:
                context = {'form': form}
                return render(request, 'base/home.html', context)
        else:
            request.session['player_id'] = player.id
            return redirect('/question/1')
    return render(request, 'base/home.html')


def question(request, id):
    try:
        player = request.session['player_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            question = Question.objects.filter(
                enable=True).order_by('id')[id - 1]
        except IndexError:
            return redirect('/ranking')
        else:
            context = {'question': question}
            if request.method == 'POST':
                answer_index = int(request.POST['answer_index'])
                if answer_index == question.answer:
                    return redirect(f'/question/{id + 1}')
                context['answer_index'] = answer_index
            return render(request, 'base/game.html', context=context)


def ranking(request):
    return render(request, 'base/end.html')
