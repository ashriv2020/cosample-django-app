
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class BlogPost(models.Model):
	def save(self, *args, **kwargs):
		if not self.slug and self.title:
			from django.utils.text import slugify
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

# Create your models here.
