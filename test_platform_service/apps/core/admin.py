from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea

from .models import Test, Question, Answer, TestResult
from .forms import BaseAnswerFormset

from nested_admin import NestedTabularInline, NestedModelAdmin


class AnswerModelInline(NestedTabularInline):
    model = Answer
    formset = BaseAnswerFormset
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }
    extra = 0


class QuestionModelInline(NestedTabularInline):
    model = Question
    inlines = [AnswerModelInline]
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }
    extra = 0


class TestModelAdmin(NestedModelAdmin):
    inlines = [QuestionModelInline]
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }


class QuestionModelAdmin(admin.ModelAdmin):
    inlines = [AnswerModelInline]


admin.site.register(Test, TestModelAdmin)
admin.site.register(Answer)
admin.site.register(TestResult)
admin.site.register(Question, QuestionModelAdmin)