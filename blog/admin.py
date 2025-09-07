from django.contrib import admin
from .models import BlogPost, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'category', 'created_at')
	list_filter = ('category', 'author')
	search_fields = ('title', 'content')
	fieldsets = (
		(None, {
			'fields': ('title', 'content', 'author', 'category')
		}),
	)
