from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime


# Create your views here.

@csrf_exempt
def submit_expense(request):

    # TODO: validate data
    token = request.POST['token']
    this_user = User.objects.filter(token__token = token).get()
    now = datetime.now()
    Expense.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)


@csrf_exempt
def submit_income(request):

    # TODO: validate data
    token = request.POST['token']
    this_user = User.objects.filter(token__token=token).get()
    now = datetime.now()
    Income.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)