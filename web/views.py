from json import JSONEncoder
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST

from .models import User, Token, Expense, Income

# Create your views here.


@csrf_exempt
@require_POST
def login(request):
    context = {}
    context['status'] = 'error'

    # check if POST objects has username and password
    if 'username' and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)

        if check_password(password, this_user.password):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            context['status'] = 'ok'
            context['token'] = this_token.token
            return JsonResponse(context, encoder=JSONEncoder)

    return JsonResponse(context, encoder=JSONEncoder)


@csrf_exempt
@require_POST
def register(request):
    context = {}
    context['message'] = ''
    context['status'] = ''

    # duplicate email
    if User.objects.filter(email=request.POST['email']).exists():
        context['message'] = 'متاسفانه این ایمیل قبلا استفاده شده است.'
        context['status'] = 'error'
        return JsonResponse(context, encoder=JSONEncoder)

    # if user does not exists
    if not User.objects.filter(username=request.POST['username']).exists():
        email = request.POST['email']
        password = make_password(request.POST['password'])
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        new_user = User.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        this_token = get_random_string(length=48)
        Token.objects.create(user=new_user, token=this_token)
        context['token'] = this_token
        context['message'] = 'ثبت نام با موفقیت انجام شد. توکن خود را میتوانید استفاده کنید.'
        context['status'] = 'ok'

    else:
        context['message'] = 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید.'
        context['status'] = 'error'

    return JsonResponse(context, encoder=JSONEncoder)


@csrf_exempt
@require_POST
def submit_expense(request):
    # TODO: validate data
    token = request.POST['token']
    this_user = User.objects.filter(token__token=token).get()
    now = datetime.now()
    Expense.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)


@csrf_exempt
@require_POST
def submit_income(request):
    # TODO: validate data
    token = request.POST['token']
    this_user = User.objects.filter(token__token=token).get()
    now = datetime.now()
    Income.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok'
    }, encoder=JSONEncoder)
