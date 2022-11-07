from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):

    email = forms.CharField(label="Адрес электронной почты",
                            widget=forms.EmailInput(attrs={"class": "form-control"}))
    subject = forms.CharField(max_length=150, label="Тема",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    body = forms.CharField(label="Текст письма",
                            widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text="Введите не более 150 символов", label="Введите ник пользователя",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Введите пароль", help_text="Пароль должен содержать минимум 8 знаков",
                            widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Введите пароль ещё раз",
                            widget=forms.PasswordInput(attrs={"class": "form-control"}))

    email = forms.CharField(label="Введите адрес электронной почты",
                            widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Введите ник пользователя",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Введите пароль",
                            widget=forms.PasswordInput(attrs={"class": "form-control"}))


# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label="Название", widget=forms.TextInput(attrs={"class": "form-control"}))
#     content = forms.CharField(label="Контент", required=False, widget=forms.Textarea(attrs={"class": "form-control",
#                                                                                             "rows": 5}))
#     is_published = forms.BooleanField(label="Опубликовать", initial=True)
#     category = forms.ModelChoiceField(empty_label="Выберите категорию", queryset=Category.objects.all(),
#                                       label="Категория", widget=forms.Select(attrs={"class": "form-control"}))
#     photo = forms.ImageField(label="Изображение", required=False)

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "photo", "is_published", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r"\d", title):
            raise ValidationError("Название не должно начинаться с цифры!")
        return title
