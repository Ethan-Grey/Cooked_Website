from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )



class UserEmailPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email'
        }),
        label='Email Address'  # Custom label for the email field
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter password'
        }),
        label='Password'  # Custom label for password1
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm password'
        }),
        label='Confirm Password'  # Custom label for password2
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered. Please use a different email or try logging in.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
            
        return cleaned_data



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        }
        labels = {
            'first_name': 'First Name',  # Custom label for first_name
            'last_name': 'Last Name',    # Custom label for last_name
            'username': 'Username'       # Custom label for username
        }






# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 
#         'placeholder': 'Enter Username',
#         'aria-label': 'Username'
#     }))
    
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'class': 'form-control', 
#         'placeholder': 'Enter Email',
#         'aria-label': 'Email'
#     }))
    
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control', 
#         'placeholder': 'Enter Password',
#         'aria-label': 'Password'
#     }))
    
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control', 
#         'placeholder': 'Confirm Password',
#         'aria-label': 'Confirm Password'
#     }))
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
