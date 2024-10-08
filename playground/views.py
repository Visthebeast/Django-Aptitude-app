from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
import random
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.decorators import login_required



def home(request):
    context = {'categories' : Category.objects.all()}

    if request.GET.get('category'):
        return redirect(f"/mcq/?category={request.GET.get('category')}")

    return render(request,'home.html',context)

# #

def mcq(request):
    name = request.GET.get('name')
    user_id = request.GET.get('user_id')
    category_name = request.GET.get('category')

    if not name or not user_id:
        return redirect('home')

    try:
        existing_user = User.objects.get(user_id=user_id)
        if existing_user.name != name:
            query_string = urlencode({'error_message': 'User ID and name does not match!!'})
            return HttpResponseRedirect(f'/?{query_string}')
    except User.DoesNotExist:
        existing_user = User.objects.create(name=name, user_id=user_id)

    try:
        category = Category.objects.get(category_name=category_name)
    except Category.DoesNotExist:
        return redirect('home')

    user_timer, created = UserTimer.objects.get_or_create(user=existing_user, category=category)
    if created:
        user_timer.remaining_time = 300  
        user_timer.save()

    context = {
        'user': existing_user,
        'category': category_name,
        'remaining_time': user_timer.remaining_time,
    }

    return render(request, 'mcq.html', context)

@csrf_exempt
def submit_mcq(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        category_name = request.POST.get('category')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
        
        try:
            category = Category.objects.get(category_name=category_name)
        except Category.DoesNotExist:
            return HttpResponse("Category not found", status=404)

        questions = Questions.objects.filter(category=category)
        score = 0
        
        max_response_number = UserResponse.objects.filter(user=user, question__category=category).aggregate(Max('response_number'))['response_number__max'] or 0
        max_response_number += 1

        for question in questions:
            selected_answer_text = request.POST.get(f'question_{question.pk}')

            try:
                selected_answer = Answer.objects.get(question=question, answer=selected_answer_text)
                correct_answer = Answer.objects.get(question=question, is_correct=True)

                if selected_answer.answer == correct_answer.answer:
                    score += question.marks


                UserResponse.objects.create(
                    user=user,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=(selected_answer.answer == correct_answer.answer),
                    response_number=max_response_number
                )
            except Answer.DoesNotExist:
                continue  

        score_obj, created = Score.objects.get_or_create(user=user, category=category)
        score_obj.score = max(score_obj.score, score)  
        score_obj.save()

        UserTimer.objects.filter(user=user, category=category).update(remaining_time=300)

        return redirect('home')

    return redirect('home')

def update_timer(request):
    user_id = request.GET.get('user_id')
    category_name = request.GET.get('category')
    remaining_time = request.GET.get('remaining_time')

    try:
        user = User.objects.get(user_id=user_id)
        category = Category.objects.get(category_name=category_name)
        user_timer = UserTimer.objects.get(user=user, category=category)
        user_timer.remaining_time = remaining_time
        user_timer.save()
    except (User.DoesNotExist, Category.DoesNotExist, UserTimer.DoesNotExist):
        return JsonResponse({'status': False})

    return JsonResponse({'status': True})

from django.shortcuts import render
from .models import User, UserResponse, Score

from django.shortcuts import render
from .models import User, UserResponse, Score, Category

@login_required
def dashboard(request):
    selected_user_id = request.GET.get('user_id')
    selected_category_name = request.GET.get('category')
    users = User.objects.all()
    categories = Category.objects.all()  
    
    if selected_user_id:
        selected_user = User.objects.get(user_id=selected_user_id)
        if selected_category_name:
            selected_category = Category.objects.get(category_name=selected_category_name)
            responses = UserResponse.objects.filter(user=selected_user, question__category=selected_category)
        else:
            responses = UserResponse.objects.filter(user=selected_user)
        
        responses_grouped = {}
        for response in responses.order_by('response_number', 'question__category'):
            if response.response_number not in responses_grouped:
                responses_grouped[response.response_number] = []
            responses_grouped[response.response_number].append(response)
        
        scores = Score.objects.filter(user=selected_user)
    else:
        selected_user = None
        responses_grouped = {}
        scores = []

    return render(request, 'dashboard.html', {
        'users': users,
        'categories': categories,
        'selected_user': selected_user,
        'selected_category': selected_category_name,
        'responses_grouped': responses_grouped,
        'scores': scores
    })



# #

def get_mcq(request):
    try:
        question_objs = Questions.objects.all()

        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains = request.GET.get('category'))

        question_objs=list(question_objs)
        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                "category":question_obj.category.category_name ,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "uid": question_obj.uid,
                "answers":question_obj.get_answers()
            })
        payload={'status' :  True, 'data' : data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")