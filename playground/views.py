from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import random

def home(request):
    return render(request,'home.html')
# Create your views here.


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