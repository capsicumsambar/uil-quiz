from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "correct_answer")
    list_filter = ("correct_answer",)
    search_fields = ("question", "option_a", "option_b", "option_c", "option_d")
