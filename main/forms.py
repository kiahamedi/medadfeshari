# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget




class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	captcha = ReCaptchaField(widget=ReCaptchaWidget())

	class Meta:
		model = User
		fields = ("username","email","password1","password2")


	def save(self,commit=True):
		user = super(NewUserForm,self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.is_staff = True
			user.save()
		return user

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
