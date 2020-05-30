from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from dashboard.models import Follow, Follower, Friend, Friend_request, Friendship
from .models import Post, Like, Comment

# Create your views here.
def discover(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'discover/discover.html', context)

def friend_request(request, username):
	friend_request = Friend_request(user = request.user, request = User.objects.get(username = username))
	friend_request.save()
	return profile(request, username)

def follow(request, username):

	follow = Follow(user = request.user, follow = User.objects.get(username=username))
	follow.save()

	follower = Follower.objects.get(user = User.objects.get(username=username))
	follower.followers += 1
	follower.save()

	return profile(request, username)

def unfollow(request, username):
	delete_follow = Follow.objects.get(user = request.user, follow = User.objects.get(username = username))
	delete_follow.delete()

	remove_follower = Follower.objects.get(user = User.objects.get(username=username))
	remove_follower.followers -= 1

	remove_follower.save()

	return profile(request, username)

def profile(request, username):
	follow_flag = False
	friend_flag = False
	friendship_flag = False

	friendships = Friendship.objects.all()
	friend_requests = Friend_request.objects.all()
	followers = Follow.objects.all()
	user = User.objects.get(username = username)

	if(user == request.user):
		return HttpResponseRedirect(reverse('discover'))

	for follow in followers:
		if(follow.user == request.user and follow.follow == user):
			follow_flag = True

	for friend in friend_requests:
		if(friend.user == request.user and friend.request == user):
			friend_flag = True

	for friendship in friendships:
		if(friendship.friend_one == request.user and friendship.friend_two == user):
			friendship_flag = True

	return render(request, 'discover/profile.html', {'user': user, 'follow_flag': follow_flag, 'friend_flag': friend_flag, 'friendship_flag': friendship_flag, 'posts': Post.objects.all()})

def comment(request, id):
	if(request.POST.get('comment')):
		update_comment = Post.objects.get(pk = id)
		update_comment.comments += 1
		update_comment.save()

		new_comment = Comment(userid = request.user, postid = update_comment, comment = request.POST['comment'])
		new_comment.save()

	context = {
		'id': id,
		'comments': Comment.objects.all()
	}
	return render(request, 'discover/comment.html', context)

def like(request, id):
	flag = False
	if(request.user.is_authenticated):
		if(Post.objects.get(pk = id).userid != request.user):
			likes = Like.objects.all()
			for like in likes:
				if(like.userid == request.user and like.postid == Post.objects.get(pk = id)):
					flag = True

			if(flag):
				update_like = Post.objects.get(pk = id)
				update_like.likes -= 1
				update_like.save()
				delete = Like.objects.get(userid = request.user, postid = Post.objects.get(pk = id))
				delete.delete()
			else:
				update_like = Post.objects.get(pk = id)
				update_like.likes += 1
				update_like.save()
				like = Like(userid = request.user, postid = update_like)
				like.save()

			return HttpResponseRedirect(reverse('discover'))
	return HttpResponseRedirect(reverse('login'))

def login_view(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('discover'))

	else:
		if(request.POST.get('user')):
			user = request.POST["user"]
			password = request.POST["password"]
			user = authenticate(request, username=user, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				return render(request, 'discover/login.html', {'message': 'Invalid credentials'})
		return render(request, 'discover/login.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('discover'))

def register(request):
	if(request.POST.get('user')):
		user = request.POST["user"]
		email = request.POST["email"]
		password = request.POST["password"]
		register_user = User.objects.create_user(user, email, password)
		register_follow = Follower(user = User.objects.get(username = user), followers = 0)
		register_follow.save()
		register_friend = Friend(user = User.objects.get(username = user), friend = 0)
		register_friend.save()

		return HttpResponseRedirect(reverse("login"))
	return render(request, 'discover/register.html')

def submit_post(request):
	post = Post(userid = request.user, likes = 0, comments = 0, post = request.POST['post'])
	post.save()
	return HttpResponseRedirect(reverse("discover"))