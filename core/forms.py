from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Address

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password'
    )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }),
        label='Username'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }),
        label='Confirm Password'
    )
    
    # Address fields
    address_line1 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 1',
        }),
        label='Address Line 1',
        required=True
    )
    address_line2 = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 2 (Optional)',
        }),
        label='Address Line 2',
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City',
        }),
        label='City',
        required=True
    )
    pincode = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pincode',
        }),
        label='Pincode',
        required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        }),
        label='Phone Number',
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create default address for the user
            Address.objects.create(
                user=user,
                label='Home',
                line1=self.cleaned_data['address_line1'],
                line2=self.cleaned_data.get('address_line2', ''),
                city=self.cleaned_data['city'],
                pincode=self.cleaned_data['pincode'],
                phone=self.cleaned_data['phone'],
                default=True
            )
        return user
