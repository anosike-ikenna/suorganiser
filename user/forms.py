import logging

from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm)
from .utils import ActivationMailFormMixin
from django.core.exceptions import ValidationError 
from django.utils.text import slugify
from .models import Profile
from django.contrib.messages import error


logger = logging.getLogger(__name__)

class ResendActivationEmailForm(ActivationMailFormMixin, forms.Form):
    
    email = forms.EmailField()

    mail_validation_error = (
        'could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email = self.cleaned_data['email'])
        except:
            logger.warning(
                'Resend Activation: No user with '
                'email: {} .'.format(
                    self.cleaned_data['email']))
            return None
        self.send_mail(user = user, **kwargs)
        return user


class UserCreationForm(ActivationMailFormMixin, BaseUserCreationForm):
    
    name = forms.CharField(
        max_length = 255,
        help_text = (
            "The name displayed on your "
            "public profile."))

    mail_validation_error = (
        "User created. Could not send activation "
        "email. Please try again later. (Sorry!)")

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ("name", "email")
    
    def clean_name(self):
        name = self.cleaned_data['name']
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        try:
            Profile.objects.get(name=name)
            raise_error = True
        except Profile.DoesNotExist:
            raise_error = False
        if name in disallowed or raise_error:
            raise ValidationError(
                "A user with that name"
                " already exists.")
        return name

    def save(self, **kwargs):
        user = super().save(commit = False)
        # if not user.pk:
        #     user.is_active = False
        #     send_mail = True
        # else:
        #     send_mail = False
        user.save()
        self.save_m2m()
        Profile.objects.update_or_create(
            user = user,
            defaults = {
                'name': self.cleaned_data['name'],
                'slug': slugify(
                    self.cleaned_data['name']),
            })
        # if send_mail:
        #     print(kwargs)
        #     me = self.send_mail(user = user, **kwargs)
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["about", "profile_image"]

class UserChangeForm(BaseUserChangeForm):
    """For UserAdmin."""

    class Meta(BaseUserChangeForm.Meta):
        model = get_user_model()