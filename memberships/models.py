from django.conf import settings #to import custom user model
from django.db import models


MEMBERSHIP_CHOICES = ( ('Enterprice', 'ent'), ('Professional', 'pro'), ('Free', 'free') ) #defining some choices for membership_type in variable to pass in method

class Membership(models.Model): #Types of Memberships available
	slug = models.SlugField()
	membership_type = models.CharField(
			choices=MEMBERSHIP_CHOICES,
			default='Free', #so everytime a membership is created the default is set Free
			max_length=30,
			)
	price = models.IntegerField(default=100)
	stripe_plan_id = models.CharField(max_length=40)

	def __str__(self):
		return self.membership_type


class UserMembership(models.Model): 
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #as setting only one membership every user
	stripe_customer_id = models.CharField(max_length=40)
	membership = models.ForeginKey(Membership, on_delete=models.SET_NULL, null = True)

	def __str__(self):
		return self.user.username


class Subscription(models.Model): # Creating a model for subscription like in Netflix
	user_membership = models.ForeginKey(UserMembership, on_delete=model)
	stripe_subscription_id = models.CharField(max_length=40)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.user_membership.user.username



