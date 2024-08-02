from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Post, Comment, Expert, Reservation, UserProfile, Payment, Question, Answer, CheckList
from .forms import PostForm, CommentForm, TestForm
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.db.models import Count

# Create your views here.

@login_required
def main_view(request):
    return render(request, 'green/main.html')

def community(request):
    category = request.GET.get('category', 'health')
    posts = Post.objects.filter(category=category)
    return render(request, 'green/community.html', {'posts': posts, 'selected_category' : category})

def mypage(request):
    user = request.user

    context = {
        'username': user.username,
        'full_name': user.get_full_name(),
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    
    return render(request, 'green/mypage.html', context)

def test(request):
    return render(request, 'green/test.html')

def list(request):
    return render(request, 'green/list.html')

def expert(request):
    return render(request, 'green/expert.html')

def market(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category_id=selected_category)
    else:
        products = Product.objects.all()
    return render(request, 'green/market.html', {
        'categories': categories,
        'products': products,
    })

def external_redirect_ptech(request):
    return redirect('https://p-techhealth.co.kr/')

def external_redirect_heymoon(request):
    return redirect('https://heymoon.net/shopping')

def external_redirect_jiguhara(request):
    return redirect('https://jiguhara.cafe24.com/')

def external_redirect_puliodays(request):
    return redirect('https://puliodays.com/product/%ED%92%80%EB%A6%AC%EC%98%A4-%EC%A2%85%EC%95%84%EB%A6%AC-%EB%A7%88%EC%82%AC%EC%A7%80%EA%B8%B0-v3/143/')

def external_redirect_costco(request):
    return redirect('https://www.costco.co.kr/BeautyHouseholdPersonal-Care/BathBodyOral-Care/Oral-Care/Red-Seal-Herbal-Toothpaste-110g-x-4/p/634452')

def community_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('green:community')
    else:
        form = PostForm()
    
    return render(request, 'green/community_create.html', {'form': form})

def community_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('green:community_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'green/community_detail.html', {'post': post, 'comments': comments, 'form': form})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('green:community_detail', post_id=post_id)

def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('green:community_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'green/add_comment_to_post.html', {'form': form})

def community_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('green:community_detail', post_id=post_id)

    return render(request, 'green/community_detail.html', {'post': post, 'comments': comments, 'form': form})

def community_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('green:community_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'green/community_update.html', {'form': form, 'post': post})

def community_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('green:community')
    
    return render(request, 'green/community_delete.html', {'post': post})

@login_required
def expert(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_premium:
            return redirect('green:premium_info')
    except UserProfile.DoesNotExist:
        return redirect('green:premium_info')

    experts = Expert.objects.all()
    return render(request, 'green/expert.html', {'experts': experts})

def reserve(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        duplicate_reservations = Reservation.objects.filter(
            expert=expert,
            user=request.user,
            date=date,
            time=time
        )
        
        if duplicate_reservations.exists():
            duplicate_reservations.exclude(id=duplicate_reservations.first().id).delete()
        
        if not duplicate_reservations.exists():
            Reservation.objects.create(
                expert=expert,
                date=date,
                time=time,
                user=request.user
            )
        
        return redirect('green:reserve_ok', expert_id=expert.id)
    
    return render(request, 'green/reserve.html', {'expert': expert})

def reserve_ok(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)
    return render(request, 'green/reserve_ok.html', {'expert': expert})

def reserve_complete(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)
    reservation = Reservation.objects.filter(expert=expert, user=request.user).latest('id')
    return render(request, 'green/reserve_complete.html', {'expert': expert, 'reservation': reservation})

def premium_info(request):
    return render(request, 'green/premium_info.html')

def premium_ok(request):
    if request.method == 'POST':
        return redirect('green:submit_payment')
    return render(request, 'green/premium_ok.html')

def submit_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id', '').strip()
        payment_code = request.POST.get('payment_code', '').strip()
        # 가상 결제 ID : 123456
        if payment_id == '123456' and payment_code == '123456':
            try:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.is_premium = True
                user_profile.save()
                return redirect('green:premium_complete')
            except Exception as e:
                print(f"Error: {e}")
                return redirect('green:premium_payment_error')
        else:
            return redirect('green:premium_payment_error')

    return render(request, 'green/submit_payment.html')

def premium_complete(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.is_premium = True
    user_profile.save()
    return render(request, 'green/premium_complete.html')

def premium_payment_error(request):
    return render(request, 'green/premium_payment_error.html')

def liked_posts(request):
    user = request.user
    posts = Post.objects.filter(likes=user)
    return render(request, 'green/liked_posts.html', {'posts': posts})

def authored_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    return render(request, 'green/authored_posts.html', {'posts': posts})

def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'green/reservation_list.html', {'reservations': reservations})

@login_required
def test_view(request):
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)
    user = request.user

    if Answer.objects.filter(user=user, date__gte=one_week_ago).exists():
        return redirect('green:result')

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

    to_do_answers = sorted(answers, key=lambda x: x.score)[:5]
    to_do_list = [ answer.question.to_do for answer in to_do_answers ]

    context = {
        'scores': scores,
        'total_score': total_score,
        'to_do_list' : to_do_list,
    }

    return render(request, 'green/result.html', context)

def detail_result_view(request):
    answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]

    result = []
    for answer in answers:
        question = answer.question
        result.append({
            'question': question.question,
            'score': answer.score,
            'tip': question.tip,
        })

    context = {
        'result': result,
    }
    return render(request, 'green/detail_result.html', context)


@login_required
def analysis_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_premium:
            return redirect('green:premium_info')
    except UserProfile.DoesNotExist:
        return redirect('green:premium_info')
    
    answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    to_do_answers = sorted(answers, key=lambda x: x.score)[:5]
    to_do_list = [ answer.question.to_do for answer in to_do_answers ]

    context = {
        'answers': answers,
        'to_do_list': to_do_list,
    }

    return render(request, 'green/analysis.html', context)

@login_required
def detail_analysis_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_premium:
            return redirect('green:premium_info')
    except UserProfile.DoesNotExist:
        return redirect('green:premium_info')
    
    latest_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    second_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[10:20]
    third_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[20:30]

    context = {
        'latest_answers': latest_answers,
        'second_answers': second_answers,
        'third_answers': third_answers,
    }

    return render(request, 'green/detail_analysis.html', context)


@login_required
def list_view(request):
    # 투두 리스트 항목
    latest_answers = Answer.objects.filter(user=request.user).order_by('-timestamp')[:10]
    answers = sorted(latest_answers, key=lambda x: x.score)[:5]

    to_do_list = [ answer.question for answer in answers ]

    # 체크 리스트
    if request.method == 'POST':
        CheckList.objects.filter(user=request.user, date=timezone.now().date()).delete()

        for question in to_do_list:
            complete = request.POST.get(f'to_do_{question.id}', '0') == '1'
            if complete:
                CheckList.objects.create(
                    user=request.user,
                    question=question,
                    date=timezone.now().date(),
                    complete=True
                )
        return redirect('green:list')

    check_list = CheckList.objects.filter(user=request.user, date=timezone.now().date())
    completed_list = {list.question.id: list.complete for list in check_list}

    # 일주일 리포트
    today = timezone.now().date()
    sunday = today - timedelta(days=today.weekday()+1) 
    saturday = sunday + timedelta(days=6)

    weekly_completion = CheckList.objects.filter(
        user=request.user,
        date__range=[sunday, saturday]
    ).values('date').annotate(completed_count=Count('id')).order_by('date')

    week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    completion_by_day = {day: 0 for day in week}
    for record in weekly_completion:
        day_of_week = (record['date'] - sunday).days  # 0(월요일) ~ 6(일요일)
        completion_by_day[week[day_of_week]] = record['completed_count']

    # 올해 리포트
    year = today.year
    january = timezone.datetime(year=year, month=1, day=1).date()
    december = timezone.datetime(year=year, month=12, day=31).date()

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