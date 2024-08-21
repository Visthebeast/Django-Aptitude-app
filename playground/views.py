from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import random

def home(request):
    context = {'categories' : Category.objects.all()}

    if request.GET.get('category'):
        return redirect(f"/mcq/?category={request.GET.get('category')}")

    return render(request,'home.html',context)

def mcq(request):
    return render(request , 'quiz.html' )

def get_mcq(request):
    try:
        question_objs = list(Questions.objects.all())
        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                "category":question_obj.category.category_name ,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "answers":question_obj.get_answers()
            })
        payload={'status' :  True, 'data' : data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")