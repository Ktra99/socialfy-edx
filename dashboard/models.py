from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follow(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user')
	follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follow')
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.user} is now following {self.follow}"

class Follower(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'followers')
	followers = models.IntegerField(default = 0)

	def __str__(self):
		return f"{self.user} has {self.followers} followers"

class Friend_request(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'friend')
	request = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'request')
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.user} has sent a friend request to {self.request}"

class Friend(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_friend')
	friend = models.IntegerField(default = 0)

	def __str__(self):
		return f"{self.user} has {self.friend} friends"

class Friendship(models.Model):
	friend_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'friend_one')
	friend_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'friend_two')
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.friend_one} is now friend with {self.friend_two}"
