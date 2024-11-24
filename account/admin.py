from django.contrib import admin
from .models import Account


# Register your models here.


class acctAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'active_investment', 'total_earnings', 'last_deposit', 'date')


admin.site.register(Account, acctAdmin)