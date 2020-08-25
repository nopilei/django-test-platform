from django.contrib import admin

from .models import TestUser
from ..core.models import TestResult


class TestResultModelInline(admin.TabularInline):
    model = TestResult
    extra = 0


class TestUserModelAdmin(admin.ModelAdmin):
    readonly_fields = ['photo']
    inlines = [TestResultModelInline]


admin.site.register(TestUser, TestUserModelAdmin)

