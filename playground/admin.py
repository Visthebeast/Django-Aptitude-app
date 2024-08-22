from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]

# #
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'score')

class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_answer', 'is_correct')

# #

admin.site.register(User, UserAdmin)
admin.site.register(UserResponse, UserResponseAdmin)

admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answer)