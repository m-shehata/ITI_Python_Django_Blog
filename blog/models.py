from __future__ import unicode_literals
from django.db import models
from django.db.models import permalink

# Create your models here.

class Categories(models.Model):
	cat_name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	sub_users = models.ManyToManyField('auth.User', blank=True,related_name='subscribed_categories')
	
	def __str__(self):
		return self.cat_name

	@permalink
	def get_absolute_url(self):
		return ('view_blog_categories', None, { 'slug': self.slug })


class Posts(models.Model):
	post_title =models.CharField(max_length=200, unique=True)
	slug=models.SlugField(max_length=200, unique=True)
	post_body =models.TextField()
	image =models.ImageField(upload_to="img/blog", blank=True)
	publish_date =models.DateTimeField(db_index=True, auto_now_add=True)
	author = models.ForeignKey('auth.User')
	category=models.ForeignKey('Categories',on_delete=models.CASCADE,related_name='posts')
	viewed = models.IntegerField(default=0)


	def __str__(self):
		return self.post_title

	@permalink
	def get_absolute_url(self):
		return ('view_blog_post', None, { 'slug': self.slug })

class Comment_Section (models.Model):
	comment_body=models.TextField()
	comment_date=models.DateTimeField(auto_now_add=True)
	#comment_usrname=models.CharField(max_length=100)
	comment_usrname=models.ForeignKey('auth.User',on_delete=models.CASCADE)
	comment_post=models.ForeignKey('Posts',on_delete=models.CASCADE, related_name='comments')

	def __str__(self):
		return self.comment_body

	def check_comment (self):
		inappr_obj=Inappropriate_words.objects.all()
		temp=""
		lst=self.comment_body.split()
		for word in lst:
			for inappr in inappr_obj:
				if word == inappr.inappr_wrd:
					word=len(word)*"*"
					break
			temp+=word
			temp+=" "
		self.comment_body=temp
		self.save()



class Inappropriate_words(models.Model):
	inappr_wrd=models.CharField(max_length=255,unique=True)
	def __str__(self):
		return self.inappr_wrd

class Reply(models.Model):
	reply_body=models.TextField()
	reply_comment=models.ForeignKey('Comment_Section', blank=True, on_delete=models.CASCADE,related_name='replies')
	reply_date=models.DateTimeField(auto_now_add=True)
	reply_username=models.ForeignKey('auth.User',on_delete=models.CASCADE)
	

	def __str__(self):
		return self.reply_body