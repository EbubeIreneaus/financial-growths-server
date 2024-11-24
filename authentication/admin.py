from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'date_joined']
    list_filter = ['date_joined', 'is_superuser']

admin.site.register(User, UserAdmin)
