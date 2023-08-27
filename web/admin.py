from django.contrib import admin
from .models import Token, Expense, Income

# Register your models here.

admin.site.register(Token)
admin.site.register(Expense)
admin.site.register(Income)
