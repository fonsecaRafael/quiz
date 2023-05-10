from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models.aggregates import Sum
from base.models import Question, Player, Reply
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
            try:
                actual_question = Reply.objects.filter(
                    player=player.id).order_by('-question')[0].question_id
                last_question = Question.objects.all().order_by('-id')[0].id
                if actual_question < last_question:
                    return redirect(f'/question/{actual_question + 1}')
                else:
                    return redirect('/ranking')
            except Reply.DoesNotExist:
                return redirect('/question/1')
    return render(request, 'base/home.html')


def ranking(request):
    try:
        player_id = request.session['player_id']
    except KeyError:
        return redirect('/')
    else:
        score_dct = Reply.objects.filter(
            player_id=player_id).aggregate(Sum('score'))
        player_score = score_dct['score__sum']

        qtd_greater_scores = Reply.objects.values('player').annotate(
            Sum('score')).filter(score__sum__gt=player_score).count()

        top_five = list(
            Reply.objects.values('player', 'player__name').annotate(
                Sum('score')).order_by('-score__sum')[:5])

        context = {
            'player_score': player_score,
            'player_position': qtd_greater_scores + 1,
            'top_five': top_five
        }
        return render(request, 'base/end.html', context)


MAX_SCORE = 1000


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
                    try:
                        first_answer_date = Reply.objects.filter(
                            question=question).order_by('answered_at')[0].answered_at
                    except IndexError:
                        Reply(player_id=player, question=question,
                              score=MAX_SCORE).save()
                    else:
                        diff = now() - first_answer_date
                        diff_in_seconds = int(diff.total_seconds())
                        score = max(MAX_SCORE - diff_in_seconds, 10)
                        Reply(player_id=player, question=question,
                              score=score).save()
                    return redirect(f'/question/{id + 1}')
                context['answer_index'] = answer_index
            return render(request, 'base/game.html', context=context)
