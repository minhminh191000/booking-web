from django import forms #import ModelForm, CharField
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from .models import CustomUser


class SignupForm(forms.ModelForm):
    password2 = forms.CharField(validators=[MinLengthValidator(8)], max_length=255)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'password', 'address']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('password2') != cleaned_data.get('password'):
    #         raise ValidationError("Passwords do not match")
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number','url_img', 'address']
    
class UpdateFormFull(forms.ModelForm):
    password2 = forms.CharField(validators=[MinLengthValidator(8)], max_length=255)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number','url_img', 'password', 'address']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user