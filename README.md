# socialfy-edx

- Your web application must be mobile-responsive.

## Bootstrap

The app is built with bootstrap components to insure that the website is responsive.

```html
<div class="row">
		<div class="col-lg-3">
			<ul id="sidenav" class="list-group">
				<li class="list-group-item" style="margin: 0 auto; border: none; padding-bottom:10%;"><i class="fas fa-user-circle fa-8x float-right"></i></li>

				<!--
				<li class="list-group-item"><form style="text-align: center; padding-bottom:10%;"><button class="btn btn-success">Follow</button></form></li>-->

				<li class="list-group-item"><a href="{% url 'post' %}">Posts</a></li>
				<li class="list-group-item">Followers <span class="badge badge-success">{{followers}}</li>
				<li class="list-group-item"><a href="{% url 'friend' %}">Friends</a></li>
			</ul>
		</div>
		<div class="col-lg-9">
			<canvas id="myChart" height="120"></canvas>	
		</div>
	</div>
```

- Your web application must utilize at least two of Python, JavaScript, and SQL.

## Python

I used the django framework to create a dynamic social media prototype

## Javascript

I used javascript to dynamically represent some of the profile values through a graph with the help of [chart.js](https://www.chartjs.org/)

```html
<script>
		let likes = "{{likes}}";
		let comments = "{{comments}}";
		let followers = "{{followers}}";
		let friends = "{{friends}}";
		let posts = "{{posts}}";
</script>

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Likes', 'Comments', 'Followers', 'Friends', 'Posts'],
        datasets: [{
            label: 'Activity',
            data: [likes, comments, followers, friends, posts],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
```

## About the project

This project was made using django. The app is seperated into two different app components (discover and dashboard). The site is made to allow people to visit without registration/login. But the functionality will be restricted to those people who have an account and are logged in.

The main functionalities of this project

- Login/register/logout functionality
- Follow/add/remove-friend functionality
- Like/comment functionality
- Dashboard setup

## Login/register/logout

I followed throughout the django introduction video and was able to construct my own version

```html
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

```

## Follow function

I have created 3 models in order to create a usuable follow functionality

```html

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

```

## Add/remove - friend

I have added an additional friend request function. Allowing the user to choose to accept a friend request or reject. The friend function consist of 3 models similar to the follow function

```html
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
```

## Like/comment

A user will not be able to like/comment his/her own content but will be able to do so on other users content. The user is also able to view who liked his content and who has commented on his post. This can be viewed within the video provided.

## Dashbaord setup

Along with the graph that i made with chartjs. I was able to construct a modern typical dashboard. With a sidebar to go with it.
