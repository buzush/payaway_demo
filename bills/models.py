from django.db import models
from datetime import date
from django.contrib.auth.models import User
from payaway.settings import *	# SERVER_PATH

# Create your models here. - chapter 5 - models and databases

class Type(models.Model):
	m_name = models.CharField(max_length=128, unique=True)			# for different types such as gas, electricity, rent, cellular..
	m_numOfBills = models.IntegerField(default=0)

	def __unicode__(self):
		return self.m_name

class Bill(models.Model):
	m_type = models.ForeignKey(Type)
	m_name = models.CharField(max_length=128)
	m_payDate = models.DateField(default=date.today)								# date the bill was payed
	m_startDate = models.DateField(default=date.today)							# the time the bill is related to
	m_endDate = models.DateField(default=date.today)
	m_price = models.IntegerField(default=0)		# the amount payed
	m_confirm = models.IntegerField(default=0)		# confirmation number
	m_image = models.URLField(max_length=200, default=SERVER_PATH + 'static/logo.gif')						# bill picture
	m_comment = models.CharField(max_length=1024, blank=True)
	picture = models.ImageField(upload_to='bills_images', blank=True)

	def __unicode__(self):
		return self.m_name
# added in chapter 8 - user authentecation
class UserProfile(models.Model):
	"""docstring for UserProfile"""
	# this line is required. Links UserProfile to a user model instance
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

