from django.contrib import admin
from .models import Categories,Posts,Comment_Section,Reply,Inappropriate_words

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('cat_name',)}

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('post_title',)}

admin.site.register(Categories, CategoryAdmin)

admin.site.register(Posts, PostAdmin)
admin.site.register(Comment_Section)
admin.site.register(Reply)
admin.site.register(Inappropriate_words)