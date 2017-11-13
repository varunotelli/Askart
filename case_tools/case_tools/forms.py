from django.contrib.auth.models import User
class Userform(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['first_name','email','password']