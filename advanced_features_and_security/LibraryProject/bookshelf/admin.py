from django.contrib import admin
from .models import Book
from .models import CustomUser
from .admin import CustomAdmin
# Register your models here.
admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')

admin.site.register(CustomUser, CustomAdmin)