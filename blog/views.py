from django.shortcuts import render,render_to_response, get_object_or_404,redirect
from models import Posts,Categories,Comment_Section,Inappropriate_words
from .forms import Categories_form, Post_Form, Comment_Form, Reply_form
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from . import forms
from django.views import generic
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .forms import RegistrationForm, RegisterForm
from .forms import Inappr_Form
# -------------------- new category --------------------------------------
def view_all_categories(request):
	all_cat = Categories.objects.all()
	context = {'all_categories':all_cat}
	return render(request,'blog/category_admin.html',context)

def add_category(request):
	form = Categories_form()
	if request.method == 'POST':
		form = Categories_form(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/blog/category/all')
	context = {'category_form':form}
	return render(request, 'blog/Categories_form.html',context )	

# -------------------- edit category --------------------------------------
def edit_category(request , slug):
	cat = Categories.objects.get(slug = slug)
	form = Categories_form(instance = cat)
	if request.method == 'POST':
		form = Categories_form(request.POST, instance = cat)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/blog/category/all')
	context = {'category_form': form}	
	return render(request, 'blog/Categories_form.html',context)

# -------------------- delete category --------------------------------------

def delete_category(request , slug):
	cat = Categories.objects.get(slug = slug)
	cat.delete()
	return HttpResponseRedirect('/blog/category/all')

# -------------------- each category_posts -----------------------------------

def view_cat_posts(request,slug):
	cat = get_object_or_404(Categories, slug = slug)
	post = cat.posts.all()
	context = {'category':cat , 'post':post}
	return render_to_response ('blog/view_cat_post.html' , context)
#-----------------------------------------------------------------------------
#bookmark
def index(request):
	all_posts= Posts.objects.all()
	all_cats= Categories.objects.all()
	paginator=Paginator(all_posts,5)
	page =request.GET.get('page')
	try:
		page_counter =paginator.page(page)
	except PageNotAnInteger:
		page_counter =paginator.page(1)
	except EmptyPage:
		page_counter =paginator.page(paginator.num_pages)
	context = {'page_counter':page_counter, 'all_cats':all_cats}
	# if request.user.is_authenticated():
	# 	logged_user=request.user
	# 	subscribed_categories=logged_user.categories_set.all()
	# 	context = {'page_counter':page_counter, 'all_cats':all_cats, 'sub_cat':subscribed_categories}

	return render(request,'blog/index.html',context)

def view_post(request,slug):
	post= Posts.objects.get(slug=slug)
	replyform=Reply_form()
	if request.method=='POST':
		print 'inside reply'
		replyform=Reply_form(request.POST)
		if replyform.is_valid():
			reply=replyform.save(commit=False)
			reply.reply_username=request.user
			reply.reply_comment=post.comments.get(id=request.POST.__getitem__('mycommentID'))
			reply.save()
			return redirect(post)


	commentform=Comment_Form()
	if request.method == "POST":
		commentform=Comment_Form(request.POST)
		if commentform.is_valid():
			print commentform
			comment=commentform.save(commit=False)
			comment.comment_post=post
			comment.comment_usrname=request.user
			comment.check_comment()
			comment.save()
			return redirect(post)
	context = {'post':post,'reply_form':replyform,'comment_form':commentform}
	return render(request,'blog/view_posts.html',context)

#----------------------- comment ------------------------------

def new_Comment(request):
	form = Comment_Form()
	if request.method == "POST":
		form = Comment_Form(request.POST)
		if form.is_valid():
			obj=form.save()
			obj.check_comment()
			return HttpResponseRedirect('/blog/comments')#m7tag yrg3 l page pta3t el post
	context={'com_form':form}
	return render(request, 'blog/newCommentForm.html', {'com_form':form})#nfs template el post

def view_all_comments(request):
	return render(request,'blog/all_comments.html')


def edit_post(request,slug):
	post=get_object_or_404(Posts,slug=slug)
	#prepopulated_fields = {'slug':('post_title',)}
	if request.method == "POST":
		form=Post_Form(request.POST,instance=post)
		if form.is_valid():
			post=form.save(commit=False)
			#post.auther=request.user
			post.publish_date=timezone.now()
			
			post.save()
			return HttpResponseRedirect('/blog/admin/posts')
			#return redirect('view_admin_posts')
	form=Post_Form(instance=post)
	context={'post_form':form}
	return render(request,'blog/postform.html',context)


def add_post(request):
	form=Post_Form()
	if request.method == 'POST':
		form=Post_Form(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return HttpResponseRedirect('/blog/admin/posts')
	context={'post_form':form}
	return render(request,'blog/postform.html',context)


def delete_post(request,slug):
	post=Posts.objects.get(slug=slug)
	Comment_Section.objects.filter(comment_post=post.id).delete()# de iterator
	post.delete()
	return HttpResponseRedirect('/blog/admin/posts')



def register(request):
	form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'],
				email=form.cleaned_data['email']
				)
			return HttpResponseRedirect('/blog/users') #url pattern bymatch el urls lw mwgood hyfire method f views

	#lw el form fadya
	
	context = {'form': form}
	return render(request,'blog/register.html',context)

	
def subscribe(request,slug):
	cat = Categories.objects.get(slug=slug)
	cat.sub_users.add(request.user)
	return HttpResponseRedirect('/blog')

def unsubscribe(request,slug):
	cat = Categories.objects.get(slug=slug)
	cat.sub_users.remove(request.user)
	return HttpResponseRedirect('/blog')


#-----------------Administration---------------------------------------

def view_all_users (request):
	users=User.objects.all()
	context={'all_users': users}
	return render (request,'blog/All_Users.html',context)

def block_users (request,user_id):	
	usr=User.objects.get(id=user_id)
	if usr.is_active is True:
		usr.is_active = False
		usr.save()
		return HttpResponseRedirect('/blog/users')
	else:
		usr.is_active = True
		usr.save()
		return HttpResponseRedirect('/blog/users')	

def delete_user (request,user_id):
	num_admins=User.objects.filter(is_superuser=True).count()
	print num_admins
	if num_admins == 1:
		print"You can't delete yourself"
		return HttpResponseRedirect('/blog/users')
	else:	
		user=User.objects.get(id=user_id)
		user.delete()
		return HttpResponseRedirect('/blog/users')
		

def promote_user(request,user_id):
	user=User.objects.get(id=user_id)
	if user.is_superuser:
		user.is_superuser = False
		user.save()

		return HttpResponseRedirect('/blog/users')

	else:
		user.is_superuser= True
	user.save()
	return HttpResponseRedirect('/blog/users')

def all_inappr(request):
	all_inappr=Inappropriate_words.objects.all()
	context={'all_inappr': all_inappr}

	return render (request,'blog/all_inappr.html',context)

def new_inappr(request):
	form = Inappr_Form()
	if request.method == "POST":
		form = Inappr_Form(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/blog/inappr')
	context={'inappr_form':form}
	return render(request, 'blog/new_inappr.html',context)



class RegisterView(generic.CreateView):
    form_class = forms.RegisterForm
    # success_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('index')
    template_name = "registration/signup.html"

def dashboard(request):
	num_cat = Categories.objects.all().count()
	num_post=Posts.objects.all().count()
	num_words=Inappropriate_words.objects.all().count()
	num_user=User.objects.all().count()
	
	context = {'num_cat':num_cat ,'num_post':num_post ,'num_words':num_words,'num_user':num_user}
	return render(request,'blog/dashboard.html',context)

def view_admin_posts(request):
	all_posts= Posts.objects.all()
	paginator=Paginator(all_posts,6)
	page =request.GET.get('page')
	try:
		context =paginator.page(page)
	except PageNotAnInteger:
		context =paginator.page(1)
	except EmptyPage:
		context =paginator.page(paginator.num_pages)
	return render(request,'blog/posts_admin.html',{'page_counter':context})