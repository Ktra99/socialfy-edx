from django.urls import path
from . import views

urlpatterns = [
	path('', views.discover, name='discover'),
	path('comment/<int:id>', views.comment, name='comment'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('submit_post', views.submit_post, name='submit_post'),
	path('like/<int:id>', views.like, name='like'),
	path('profile/<str:username>', views.profile, name='profile'),
	path('follow/<str:username>', views.follow, name='follow'),
	path('unfollow/<str:username>', views.unfollow, name='unfollow'),
	path('friend_request/<str:username>', views.friend_request, name='friend_request')
]