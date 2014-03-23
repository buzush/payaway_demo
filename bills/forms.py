from django import forms
from django.contrib.auth.models import User		# chapter 8 - user authentication
from bills.models import Type, Bill, UserProfile
from datetime import date

class TypeForm(forms.ModelForm):
	m_name = forms.CharField(max_length=128, help_text="Please enter the type name.")
	m_numOfBills = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and a model
		model = Type

class BillForm(forms.ModelForm):
	m_name = forms.CharField(max_length=128, help_text="Please enter the name of the bill:")
	m_startDate = forms.DateField(help_text="Start Date:")
	m_endDate = forms.DateField(help_text="End Date:")
	m_payDate = forms.DateField(help_text="Pay Date:", initial=date.today)
	m_price = forms.IntegerField(help_text="Price:", initial=0)
	m_comment = forms.CharField(help_text="Add comments:", required=False)
	picture = forms.ImageField(help_text="Add picture:", required=False)
	# m_image = forms.URLField(max_length=200, help_text="Please enter the URL of the bill.")

	# def clean(self):
	# 	cleaned_data = self.cleaned_data
	# 	m_image = cleaned_data.get('m_image')

	# 	# if m_image URL is not empty and doesn't start with 'http://', prepend 'http://'
	# 	# if m_image and not m_image.startwith('http://'):
	# 	# 	m_image = 'http://' + m_image
	# 	# 	cleaned_data['m_image'] = m_image

	# 	return cleaned_data


	class Meta:
		# Provide an association between the ModelForm and a model
		model = Bill
		# What fields do we want to include in our form?
		# This way we don't need every field in the model present.
		# Some fields may allow NULL values, so we may not want to include them...
		fields = ('m_name', 'm_startDate', 'm_endDate', 'm_payDate', 'm_price', 'm_comment', 'picture')

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Please enter a username.")
	email = forms.CharField(help_text="Please enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
	website = forms.URLField(help_text="Please enter your website.", required=False)
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

	class Meta:
		model = UserProfile
		fields = ['website', 'picture']
