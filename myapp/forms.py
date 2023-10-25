from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser,Product

class SignupForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin User'),
        ('normal', 'Normal User'),
    )

    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    email = forms.EmailField(max_length=254, help_text='Enter your email address')
    first_name = forms.CharField(max_length=30, help_text='Enter your first name')
    last_name = forms.CharField(max_length=30, help_text='Enter your last name')
    phone_number = forms.CharField(max_length=15, help_text='Enter your phone number')
    gender = forms.ChoiceField(choices=CHOICES, required=False)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, initial='normal')

    class Meta:
        model = MyUser
        fields = ['user_type','username', 'email', 'first_name', 'last_name','phone_number','gender','password1', 'password2']

    labels = {
        'username': 'Username',
        'email': 'Email',
        'password1': 'Password',
        'password2': 'Confirm Password',
    }

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'price', 'description', 'last_price_update_date']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'last_price_update_date': forms.TextInput(attrs={'type':'datetime-local'}),
            
        }
        labels = {
            'name' : 'Enter Product Name:',
            'image': 'Select an Image: ',
            'category': 'Select Category: ',
            'price': 'Enter a price: ',
            'description': 'Enter a Description: ',
            'last_price_update_date': 'Enter Last Price Update Date: ',
        }