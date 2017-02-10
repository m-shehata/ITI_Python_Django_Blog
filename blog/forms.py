from django import forms
from .models import Comment_Section, Categories, Posts, Reply
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inappropriate_words
from django.contrib.auth import authenticate, login, logout, get_user_model

class Comment_Form(forms.ModelForm):
	class Meta:
		model=Comment_Section
		fields=('comment_body',)


class Categories_form(forms.ModelForm):
	class Meta:
		model = Categories
		fields = ('cat_name','slug',)
		labels = {
            'cat_name': _('Category Name'),
        }
        help_texts = {
            'cat_name': _("Category name describes it's content."),
        }

class Post_Form(forms.ModelForm):
	class Meta:
		model=Posts
		fields=('post_title','slug','post_body','image','category',)

class Reply_form(forms.ModelForm):
	class Meta:
		model=Reply
		fields=('reply_body',)
        labels = {
            'reply_body': _('Enter your reply:'),
        }

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',widget=forms.TextInput(attrs=dict(max_length=30)),label='Username',error_messages={'invalid':_("Username must contain only letters, numbers and underscores.")})
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=dict(max_length=30, render_value=False)))
    password_confirm = forms.CharField(label='Password (Again)', widget=forms.PasswordInput(attrs=dict(render_value=False)))

    def clean_username(self):
    	try:
    	    user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("Username already exists. Please try another one."), code='username_exists')
 

    def clean_password_confirm(self):
    	if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
            if password == password_confirm :
                return self.cleaned_data['password_confirm']
        raise forms.ValidationError(_("Password fields don't match."), code='password_not_matched')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
    	model=User
    	fields=['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "User Name"
        self.fields["email"].label = "Email Address"
    def clean_email(self):
    	try:
    	    user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("Email is already registered by another account. Please try another one."), code='email_exists')

class Inappr_Form(forms.ModelForm):
    class Meta:
        model=Inappropriate_words
        fields=('inappr_wrd',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)