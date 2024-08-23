from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
import random
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode



def home(request):
    context = {'categories' : Category.objects.all()}

    if request.GET.get('category'):
        return redirect(f"/mcq/?category={request.GET.get('category')}")

    return render(request,'home.html',context)

# #
def mcq(request):
    name = request.GET.get('name')
    user_id = request.GET.get('user_id')
    category = request.GET.get('category')

    if not name or not user_id:
        return redirect('home')

    # Check if the user_id already exists in the system
    try:
        existing_user = User.objects.get(user_id=user_id)
        if existing_user.name != name:
            # User ID exists but name does not match
            query_string = urlencode({'error_message': 'User ID and name does not match!!'})
            return HttpResponseRedirect(f'/?{query_string}')
    except User.DoesNotExist:
        # User ID does not exist, create a new user
        User.objects.create(name=name, user_id=user_id)

    context = {
        'user': User.objects.get(user_id=user_id),
        'category': category,
    }

    return render(request, 'mcq.html', context)

@csrf_exempt
def submit_mcq(request):
    print(request.POST)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        category_name = request.POST.get('category')
        print("hoorrrAAY")
        print(category_name)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
        
        try:
            category = Category.objects.get(category_name=category_name)
        except Category.DoesNotExist:
            return HttpResponse("Category not found", status=404)

        questions = Questions.objects.all()
        score = 0

        for question in questions:
            selected_answer_text = request.POST.get(f'question_{question.pk}')

            try:
                selected_answer = Answer.objects.get(question=question, answer=selected_answer_text)
                correct_answer = Answer.objects.get(question=question, is_correct=True)

                if selected_answer.answer == correct_answer.answer:
                    score += question.marks
                    print("correct answer")

                # Save the user's response
                UserResponse.objects.create(
                    user=user,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=(selected_answer.answer == correct_answer.answer)
                )
            except Answer.DoesNotExist:
                print(f"Answer not found for question ID: {question.pk} and selected answer: {selected_answer_text}")
                continue  

        # Save the score to the user's record
        score_obj, created = Score.objects.get_or_create(user=user, category=category)
        score_obj.score = max(score_obj.score, score)  # Update only if the new score is higher
        score_obj.save()

        return redirect('home')

    return redirect('home')
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