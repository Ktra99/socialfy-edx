from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('post', views.post, name='post'),
	path('delete_post/<int:id>', views.delete_post, name='delete_post'),
	path('people_who_liked/<int:id>', views.people_who_liked, name='people_who_liked'),
	path('friend', views.friend, name='friend'),
	path('friend_accept/<str:username>', views.friend_accept, name='friend_accept'),
	path('friend_reject/<str:username>', views.friend_reject, name='friend_reject'),
]