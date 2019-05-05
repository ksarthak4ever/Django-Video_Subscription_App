from django.conf import settings #to import custom user model
from django.db import models
from django.db.models.signals import post_save

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

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
	membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null = True)

	def __str__(self):
		return self.user.email

''' django signal code '''
def post_save_usermembership_create(sender, instance, created, *args, **kwargs): #assigning a stripe plan id to each user membership as told in stripe docs.
	if created:
		UserMembership.objects.get_or_create(user=instance)

	user_membership, created = UserMembership.objects.get_or_create(user=instance)

	if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '': #i.e no stripe customer id currently allocated to this user	
		new_customer_id = stripe.Customer.create(email=instance.email) #as said in the stripe docs
		UserMembership.stripe_customer_id = new_customer_id['id']
		user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model): # Creating a model for subscription like in Netflix
	user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
	stripe_subscription_id = models.CharField(max_length=40)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.user_membership.user.username



