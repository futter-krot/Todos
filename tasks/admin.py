from django.contrib import admin
from tasks.views import delete_queryset

from tasks.models import *


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')
    fields = ('description', 'is_completed', 'owner', 'priority', 'category', 'doH', 'doM', 'doL')
    actions = [delete_queryset]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'todos_count')

@admin.register(CounterMedium)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(CounterHigh)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(CounterLow)
class CategoryAdmin(admin.ModelAdmin):
    pass