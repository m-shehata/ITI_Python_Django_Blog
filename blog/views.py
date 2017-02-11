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
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
# -------------------- new category --------------------------------------
def view_all_categories(request):
	if request.user.is_superuser:
		all_cat = Categories.objects.all()
		context = {'all_categories':all_cat}
		return render(request,'blog/category_admin.html',context)
	return HttpResponseRedirect('/blog/login')

def add_category(request):
	if request.user.is_superuser:
		form = Categories_form()
		if request.method == 'POST':
			form = Categories_form(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/blog/category/all')
		context = {'category_form':form}
		return render(request, 'blog/Categories_form.html',context )	
	return HttpResponseRedirect('/blog/login')

# -------------------- edit category --------------------------------------
def edit_category(request , slug):
	if request.user.is_superuser:
		cat = Categories.objects.get(slug = slug)
		form = Categories_form(instance = cat)
		if request.method == 'POST':
			form = Categories_form(request.POST, instance = cat)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/blog/category/all')
		context = {'category_form': form}	
		return render(request, 'blog/Categories_form.html',context)
	return HttpResponseRedirect('/blog/login')
# -------------------- delete category --------------------------------------

def delete_category(request , slug):
	if request.user.is_superuser:
		cat = Categories.objects.get(slug = slug)
		cat.delete()
		return HttpResponseRedirect('/blog/category/all')
	return HttpResponseRedirect('/blog/login')

# -------------------- each category_posts -----------------------------------

def view_cat_posts(request,slug):
	cat = get_object_or_404(Categories, slug = slug)
	post = cat.posts.all()
	context = {'category':cat , 'post':post}
	return render (request,'blog/view_cat_post.html' , context)
#-----------------------------------------------------------------------------
#bookmark
def index(request):
	all_posts= Posts.objects.all().order_by('-publish_date')
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
	post.viewed +=1
	post.save()
	replyform=Reply_form()
	if request.method=='POST':
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
	if request.user.is_superuser:
		post=get_object_or_404(Posts,slug=slug)
		#prepopulated_fields = {'slug':('post_title',)}
		if request.method == "POST":
			form=Post_Form(request.POST,request.FILES,instance=post)
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

	return HttpResponseRedirect('/blog/login')


def add_post(request):
	if request.user.is_superuser:
		form=Post_Form()
		if request.method == 'POST':
			form=Post_Form(request.POST,request.FILES)
			if form.is_valid():
				post=form.save(commit=False)
				post.author=request.user
				post.save()
				return HttpResponseRedirect('/blog/admin/posts')
		context={'post_form':form}
		return render(request,'blog/postform.html',context)
	return HttpResponseRedirect('/blog/login')


def delete_post(request,slug):
	if request.user.is_superuser:
		post=Posts.objects.get(slug=slug)
		Comment_Section.objects.filter(comment_post=post.id).delete()# de iterator
		post.delete()
		return HttpResponseRedirect('/blog/admin/posts')
	return HttpResponseRedirect('/blog/login')



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
	if request.user.is_superuser:
		users=User.objects.all()
		context={'all_users': users}
		return render (request,'blog/All_Users.html',context)
	return HttpResponseRedirect('/blog/login')

def block_users (request,user_id):
	if request.user.is_superuser:	
		usr=User.objects.get(id=user_id)
		if usr.is_active is True:
			usr.is_active = False
			usr.save()
			return HttpResponseRedirect('/blog/users')
		else:
			usr.is_active = True
			usr.save()
			return HttpResponseRedirect('/blog/users')
	return HttpResponseRedirect('/blog/login')	

def delete_user (request,user_id):
	if request.user.is_superuser:
		num_admins=User.objects.filter(is_superuser=True).count()
		if num_admins == 1:
			print"You can't delete yourself"
			return HttpResponseRedirect('/blog/users')
		else:	
			user=User.objects.get(id=user_id)
			user.delete()
			return HttpResponseRedirect('/blog/users')

	return HttpResponseRedirect('/blog/login')
		

def promote_user(request,user_id):
	if request.user.is_superuser:
		user=User.objects.get(id=user_id)
		if user.is_superuser:
				user.is_superuser = False
				user.save()
				return HttpResponseRedirect('/blog/users')
	
		else:
			user.is_superuser= True
			user.save()
			return HttpResponseRedirect('/blog/users')
	return HttpResponseRedirect('/blog/login')

def all_inappr(request):
	if request.user.is_superuser:
		all_inappr=Inappropriate_words.objects.all()
		context={'all_inappr': all_inappr}
	
		return render (request,'blog/all_inappr.html',context)
	return HttpResponseRedirect('/blog/login')

def new_inappr(request):
	if request.user.is_superuser:
		form = Inappr_Form()
		if request.method == "POST":
			form = Inappr_Form(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/blog/inappr')
		context={'inappr_form':form}
		return render(request, 'blog/new_inappr.html',context)

	return HttpResponseRedirect('/blog/login')



class RegisterView(generic.CreateView):
    form_class = forms.RegisterForm
    # success_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('index')
    template_name = "registration/signup.html"

def dashboard(request):
	if request.user.is_superuser:
		num_cat = Categories.objects.all().count()
		num_post=Posts.objects.all().count()
		num_words=Inappropriate_words.objects.all().count()
		num_user=User.objects.all().count()
		context = {'num_cat':num_cat ,'num_post':num_post ,'num_words':num_words,'num_user':num_user}
		return render(request,'blog/dashboard.html',context)

	return HttpResponseRedirect('/blog/login')

def view_admin_posts(request):
	if request.user.is_superuser:
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

	return HttpResponseRedirect('/blog/login')

	#------------------- authentication on login -----------------------------

def my_login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/blog')



    form = forms.LoginForm()
    errMsg = ""
    
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if not form.is_valid() or form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            errMsg = ""
            active = False
            is_user = False
            try:
                user = User.objects.get(username=username)
                is_user = True
                
            except Exception:
               
                errMsg += "<div class =\"alert alert-danger\" role=\"alert\" ><p>"+"User doesn't Exist!"+"</p></div>"

                
                return render(request, "registration/login.html", {'form': form, 'err':errMsg})
            else:
                if not check_password(password, user.password):

                    errMsg += "<div class =\"alert alert-danger\" role=\"alert\" ><p>" + "Check Your Password, and try again." + "</p></div>"
                    
                    return render(request, "registration/login.html", {'form': form, 'err':errMsg})
                else:
                    active = user.is_active
                    
                    if is_user and active:
                        
                        login(request, user)
                       
                        return HttpResponseRedirect('/blog')
                    else:
                        errMsg += "<div class =\"alert alert-danger\" role=\"alert\" ><p>" + "You are blocked, contact the admin." + "</p></div>"
                        return render(request, "registration/login.html", {'form': form, 'err':errMsg})
    return render(request, "registration/login.html", {'form': form, 'err':errMsg})    