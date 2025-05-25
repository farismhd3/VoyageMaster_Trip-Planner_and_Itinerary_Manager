from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Register

class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Register
        fields = ['username', 'email', 'phone', 'place', 'profile_image', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        help_texts = {'username': None}

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise forms.ValidationError("Phone number is required.")

        # Ensure phone is treated as a string
        phone = str(phone).strip()

        # Validate the phone number with regex
        phone_validator = RegexValidator(
            regex=r'^[6-9]\d{9}$',
            message="Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long."
        )

        try:
            phone_validator(phone)
        except ValidationError as e:
            raise forms.ValidationError(e.message)

        # Ensure the phone is exactly 10 digits
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")

        return phone
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data



class TravelAgencyRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    
    class Meta:
        model = Register
        fields = ['username', 'email',  'phone', 'place', 'profile_image', 'experience', 'password','certifications']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agency Name'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience in Travel Industry'}),
        }
        help_texts = {'username': None}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    

class GuideRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    
    class Meta:
        model = Register
        fields = [
            'username', 'email',  'phone', 'place', 'profile_image', 'experience', 
            'languages_spoken', 'guide_license', 'certifications', 'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            'languages_spoken': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Languages Spoken'}),
            'guide_license': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Number'}),
            'certifications': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        help_texts = {'username': None}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [ 'email', 'phone', 'place','profile_image']
         
        widgets = {
            
            "email" : forms.EmailInput,
            "phone" : forms.TextInput,
            "place" : forms.TextInput
            
           }
        help_texts={
            "username":None
        }

class LoginForm(forms.ModelForm):

    class Meta:
        model = Register
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            "password": forms.PasswordInput(attrs={"class":"form-control bg-transparent pswd"}),
           
           }
        help_texts = {'username':None}

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,  # Set required to False to bypass required validation
        widget=forms.TextInput(attrs={'class': 'form-group'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Optionally, you can add custom cleaning logic here
        return cleaned_data

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )

    

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("The password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("The password must contain at least one letter.")
        
        # Add custom validation logic here
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        self.validate_password(new_password1)
        return new_password1
       
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        # Ensure the new password is different from the old password
        if old_password and new_password1 and old_password == new_password1:
            self.add_error('new_password1', "The new password must be different from the old password.")
        
        return cleaned_data
   