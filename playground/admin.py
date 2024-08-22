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
    list_display = ('name', 'user_id', 'get_category_scores')

    def get_category_scores(self, obj):
        scores = obj.score_set.all()
        return ", ".join([f"{score.category.category_name}: {score.score}" for score in scores])

    get_category_scores.short_description = 'Scores by Category'


class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_answer', 'is_correct')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score')
    list_filter = ('category',)

# #

admin.site.register(Score, ScoreAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(UserResponse, UserResponseAdmin)

admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answer)