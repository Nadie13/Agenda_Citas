from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Fieldset

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user','image']

    

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper=FormHelper()
        self.helper.form_tag=False
        self.helper.layout=Layout(
            Fieldset(
                'Información del Perfil',
                'telephone',
                'notas_internas'
                
            )
        )