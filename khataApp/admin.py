from django.contrib import admin
from .models import CustomUser, Worker, DailyWage, MonthWageGiven, TestTable

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'first_name', 'last_name',)
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    ordering = ('first_name',)

# Register your models here.
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Worker)
admin.site.register(DailyWage)
admin.site.register(MonthWageGiven)
admin.site.register(TestTable)