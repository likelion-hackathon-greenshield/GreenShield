from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TestForm
from .models import Question, Answer, CheckList
from django.db.models import Count
from datetime import date, datetime, timedelta

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
    today = timezone.now().date()
    user = request.user

    if Answer.objects.filter(user=user, date=today).exists():
        return redirect('green:list')

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

    latest_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    answers = sorted(latest_answers, key=lambda x: x.score)[:5]

    answer_list = [ answer.question for answer in answers ]

    second_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[10:20]
    third_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[20:30]

    context = {
        'scores': scores,
        'total_score': total_score,
        'answer_list' : answer_list,
        'second_answers': second_answers,
        'third_answers': third_answers,
    }

    return render(request, 'green/result.html', context)

@login_required
def detail_result_view(request):
    latest_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    second_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[10:20]
    third_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[20:30]

    context = {
        'latest_answers': latest_answers,
        'second_answers': second_answers,
        'third_answers': third_answers,
    }

    return render(request, 'green/detail_result.html', context)


@login_required
def list_view(request):
    # 투두 리스트 항목
    latest_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    answers = sorted(latest_answers, key=lambda x: x.score)[:5]

    to_do_list = [ answer.question for answer in answers ]

    # 체크 리스트
    if request.method == 'POST':
        CheckList.objects.filter(user=request.user, date=date.today()).delete()

        for question in to_do_list:
            complete = request.POST.get(f'to_do_{question.id}', '0') == '1'
            if complete:
                CheckList.objects.create(
                    user=request.user,
                    question=question,
                    date=date.today(),
                    complete=True
                )
        return redirect('green:list')

    check_list = CheckList.objects.filter(user=request.user, date=date.today())
    completed_list = {list.question.id: list.complete for list in check_list}

    # 일주일 리포트
    today = datetime.now().date()
    sunday = today - timedelta(days=today.weekday())
    saturday = sunday + timedelta(days=6)

    weekly_completion = CheckList.objects.filter(
        user=request.user,
        date__range = [sunday, saturday]
    ).values('date').annotate(completed_count=Count('id')).order_by('date')

    week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    completion_by_day = {day: 0 for day in week}
    for record in weekly_completion:
        day_of_week = (record['date'] - sunday).days  # 0(일요일) ~ 6(토요일)
        completion_by_day[week[day_of_week]] = record['completed_count']

    # 올해 리포트
    year = today.year
    january = date(year=year, month=1, day=1)
    december = date(year=year, month=12, day=31)

    monthly_completion = CheckList.objects.filter(
        user=request.user,
        date__range=[january, december]
    ).values('date__year', 'date__month').annotate(completed_count=Count('id')).order_by('date__year', 'date__month')

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    completion_by_month = {month: 0 for month in months}
    for record in monthly_completion:
        month_num = record['date__month'] - 1
        month = months[month_num]     
        completion_by_month[month] = record['completed_count']

    context = {
        'to_do_list': to_do_list,
        'completed_list': completed_list,
        'completion_by_day': completion_by_day,
        'completion_by_month': completion_by_month,
        'today': today,
    }

    return render(request, 'green/list.html', context)