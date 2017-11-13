from django.contrib.auth.models import User
from django import forms
class Userform(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['first_name','last_name','username','password']

class Loginform(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [ 'username', 'password']