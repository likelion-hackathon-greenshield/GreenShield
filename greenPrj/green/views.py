from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TestForm
from .models import Question, Answer

# Create your views here.

@login_required
def main_view(request):
    return render(request, 'green/main.html')

def community(request):
    return render(request, 'green/community.html')

def mypage(request):
    return render(request, 'green/mypage.html')

def test(request):
    return render(request, 'green/test.html')

def list(request):
    return render(request, 'green/list.html')

def expert(request):
    return render(request, 'green/expert.html')

def market(request):
    return render(request, 'green/market.html')

@login_required
def test_view(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            for question in questions:
                score = form.cleaned_data.get(f'question_{question.id}')
                Answer.objects.create(
                    user=request.user,
                    question=question,
                    score=score,
                )
            return redirect('green:result')
    else:
        form = TestForm()

    context = {
        'form': form,
    }
    return render(request, 'green/test.html', context)

@login_required
def result_view(request):
    answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    scores = {answer.question.id: answer.score for answer in answers}
    total_score = sum(int(score) for score in scores.values())
    to_do_list = []

    for answer in answers:
        if answer.score <= 3:
            to_do_list.append(answer.question.to_do)

    return render(request, 'green/result.html', {'scores': scores, 'total_score': total_score, 'to_do_list' : to_do_list,})

@login_required
def list_view(request):
    answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]

    to_do_list = []

    for answer in answers:
        if answer.score <= 3:
            to_do_list.append(answer.question.to_do)

    return render(request, 'green/list.html', {'to_do_list' : to_do_list,})