from ckeditor.fields import RichTextFormField
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import TextInput, EmailInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe

import product
from home.models import UserProfile
from product.models import Product, Images


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }


class ProductForm(forms.ModelForm):
    detail = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = (
            'category', 'ekleyen', 'title', 'keywords', 'description', 'image', 'price', 'amount', 'detail', 'slug',
            'status')
        widgets = {
            'category': Select(attrs={'class': 'input', 'name': 'category', 'placeholder': 'category'}),
            'ekleyen': Select(attrs={'class': 'input', 'name': 'ekleyen', 'placeholder': 'ekleyen'}),
            'title': TextInput(attrs={'class': 'input', 'name': 'title', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'name': 'keywords', 'placeholder': 'keywords'}),
            'image': FileInput(attrs={'class': 'input', 'name': 'image', 'placeholer': 'image'}),
            'description': TextInput(attrs={'class': 'input', 'name': 'description', 'placeholder': 'description'}),
            'price': TextInput(attrs={'class': 'input', 'name': 'price', 'placeholder': 'price'}),
            'amount': TextInput(attrs={'class': 'input', 'name': 'amount', 'placeholder': 'amount'}),
            'slug': TextInput(attrs={'class': 'input', 'name': 'slug', 'placeholder': 'slug'}),
            'status': Select(attrs={'class': 'input', 'name': 'status', 'placeholder': 'status'}),
        }

        def image_tag(self):
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

        image_tag.short_description = 'Image'

        def get_absolute_url(self):
            return reverse('product_detail', kwargs={'slug': self.slug})
