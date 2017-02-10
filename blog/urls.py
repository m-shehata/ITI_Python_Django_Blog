
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^login/$',views.my_login_view, name='my_login_view'),

    url('^', include('django.contrib.auth.urls')),

    url(r'^$',views.index, name='index'),
    url(r'^register-user/$',views.RegisterView.as_view(), name='signup'),
    url(r'^register/$',views.register, name='register'),
    url(r'^category/new$',views.add_category,name='add_category'),#aked mkanha 3nd eladmin
    url(r'^category/all$',views.view_all_categories , name = 'view_all_categories'),
    url(r'^category/(?P<slug>[-\w]+)/$',views.view_cat_posts, name='view_blog_categories'),
	url(r'^category/(?P<slug>[-\w]+)/edit$',views.edit_category,name='edit_category'),
    url(r'^category/(?P<slug>[-\w]+)/delete$',views.delete_category,name='delete_category'),
    url(r'^post/new$',views.add_post,name='add_post'),#aked de mkanha msh hna de 3nd el admin
    url(r'^post/(?P<slug>[-\w]+)$',views.view_post,name='view_blog_post'),
    url(r'^post/(?P<slug>[-\w]+)/edit$',views.edit_post,name='edit_post'),
    url(r'^post/(?P<slug>[-\w]+)/delete$',views.delete_post,name='delete_post'),
    url(r'^category/(?P<slug>[-\w]+)/subscribe$',views.subscribe,name='subscribe'),
    url(r'^category/(?P<slug>[-\w]+)/unsubscribe$',views.unsubscribe,name='unsubscribe'),
    url(r'^comments$',views.view_all_comments),
    url(r'^comments/new$',views.new_Comment),
    url(r'^admin$',views.dashboard ,name='dashboard'),
    url(r'^admin/posts$',views.view_admin_posts,name='view_admin_posts'),
    url(r'^users$',views.view_all_users,name='all_users'),
    url(r'^users/(?P<user_id>[0-9]+)/blocking$',views.block_users,name='view_block_user'),
    url(r'^users/(?P<user_id>[0-9]+)/delete$',views.delete_user,name='view_delete_user'),
    url(r'^users/(?P<user_id>[0-9]+)/promote$',views.promote_user,name='view_promote_user'),
    url(r'^inappr$',views.all_inappr,name='all_inappr'),
    url(r'^inappr/new$',views.new_inappr,name='new_inappr')
    

    
]

