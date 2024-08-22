from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import random
from django.views.decorators.csrf import csrf_exempt


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

    user, created = User.objects.get_or_create(name=name, user_id=user_id)

    context = {
        'user': user,
        'category': category,
    }

    return render(request, 'mcq.html', context)

@csrf_exempt
def submit_mcq(request):
    print(request.POST)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)

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
                continue  # Skip to the next question if the answer is not found

        # Save the score to the user's record
        user.score = max(score,user.score)
        user.save()

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