from django import forms
from django.contrib.auth import get_user_model
from mptt.forms import TreeNodeChoiceField
from .models import AddressGlobal
from accounts.models import State

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=200,required=False)
    country = forms.CharField(max_length=200, required=False)
    password1 = forms.CharField(label="Password",max_length=62,widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password",max_length=62,widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email','name','password1','password2','phone_number','country']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")


class AddressForm(forms.ModelForm):
    state = TreeNodeChoiceField(queryset=State.objects.filter(level=0))
    city = forms.CharField(max_length=250,widget=forms.Select(attrs={'class': 'form-select'}))
    address = forms.CharField(max_length=500,label='Address',widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = AddressGlobal
        fields = ("address",'city','state')

class AddressEditForm(forms.ModelForm):
    class Meta:
        model = AddressGlobal
        fields = ('address','city','state')
