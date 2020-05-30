from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	comments = models.IntegerField(default=0)
	post = models.CharField(max_length = 500)
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.post} posted by {self.userid}"

class Like(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	postid = models.ForeignKey(Post, on_delete=models.CASCADE)
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.userid} liked {self.postid}"

class Comment(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	postid = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.CharField(max_length = 500)
	date = models.DateField(auto_now = True)

	def __str__(self):
		return f"{self.userid} commented {self.comment} on the post {self.postid}"
