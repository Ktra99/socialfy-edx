from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from discover.models import Post, Like, Comment
from .models import Follow, Follower, Friendship, Friend_request, Friend

# Create your views here.
def dashboard(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	else:

		like_count = 0
		comment_count = 0
		post_count = 0

		likes = Like.objects.filter(userid = request.user)
		comments = Comment.objects.filter(userid = request.user)
		posts = Post.objects.filter(userid = request.user)

		for like in likes:
			like_count += 1

		for comment in comments:
			comment_count += 1

		for post in posts:
			post_count += 1

		context = {
			'likes': like_count,
			'comments': comment_count,
			'followers': Follower.objects.get(user = request.user).followers,
			'friends': Friend.objects.get(user = request.user).friend,
			'posts': post_count
		}
		return render(request, 'dashboard/dashboard.html', context)

def post(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'dashboard/post.html', context)

def delete_post(request, id):
	post = Post.objects.get(pk = id)
	post.delete()
	return HttpResponseRedirect(reverse('post'))

def people_who_liked(request, id):
	context = {
		'likes': Like.objects.all(),
		'post': Post.objects.get(pk = id)
	}

	return render(request, 'dashboard/people_who_liked.html', context)

def friend(request):
	context = {
		'friends': Friendship.objects.all(),
		'friend_requests': Friend_request.objects.all()
	}
	return render(request, 'dashboard/friend.html', context)

def friend_accept(request, username):

	close = Friend_request.objects.get(user = User.objects.get(username = username), request = request.user)
	close.delete()

	friends = Friendship(friend_one = request.user, friend_two = User.objects.get(username = username))
	friends.save()

	friend_count = Friend.objects.get(user = request.user)
	friend_count.friend += 1
	friend_count.save()

	other_friend_count = Friend.objects.get(user = User.objects.get(username = username))
	other_friend_count.friend += 1
	other_friend_count.save()

	return HttpResponseRedirect(reverse('friend'))

def friend_reject(request, username):

	close = Friend_request.objects.get(user = User.objects.get(username = username), request = request.user)
	close.delete()

	return HttpResponse("Rejected")


