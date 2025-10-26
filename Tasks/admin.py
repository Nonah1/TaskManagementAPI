from django.contrib import admin
from .models import Task, User, Notification

# Register your models here.
#task admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'priority', 'due_date', 'completed_at')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-due_date',)


#user admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)


#notificarion
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('message', 'user__username')
    ordering = ('-created_at',)
