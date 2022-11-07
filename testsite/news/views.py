from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserLoginForm, ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout

from .forms import NewsForm
from .models import News, Category


def send_mails_to_user(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data["subject"], form.cleaned_data["body"], "my_almond_cat@mail.ru",
                             [form.cleaned_data["email"]], fail_silently=False)
            if mail:
                messages.add_message(request, messages.SUCCESS, "Письмо отправлено")
                return redirect("home")
            else:
                messages.add_message(request, messages.ERROR, "Письмо не отправлено")
        else:
            messages.add_message(request, messages.ERROR, "Что-то пошло не так :(")
    else:
        form = ContactForm()
    return render(request, "news/mail_to_user.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Регистрация прошла успешно")
            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "Что-то пошло не так :(")
    else:
        form = UserRegisterForm()
    return render(request, "news/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Авторизация прошла успешно")
            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "Что-то пошло не так :(")
    else:
        form = UserLoginForm()
    return render(request, "news/login.html", context={"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


class HomeNews(ListView):
    model = News
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная"
        return context

    def get_queryset(self):
        return News.objects.select_related('category')


class NewsOfCategory(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news"
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["category_id"]).select_related('category')


class ViewNews(DetailView):
    model = News
    #pk_url_kwarg = "news_id"
    #template_name = "news/news_detail.html"
    context_object_name = "news_item"


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    login_url = "/admin/"


# def get_news(request, news_id):                               # открыть новость
#     news_obj = get_object_or_404(News, pk=news_id)
#     context = {"news_obj": news_obj,
#                "title": news_obj.title,
#                "content": news_obj.content,
#                "date": news_obj.date,
#                "photo": news_obj.photo,
#                "category": news_obj.category,
#                }
#     return render(request, "news/news_item.html", context)


# def get_category(request, category_id):                          # новости по категориям
#     news = News.objects.filter(category_id=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     context = {"news": news,
#                "title": category.name,
#                "category": category,
#                }
#     return render(request, "news/categories.html", context)


# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, "news/add_news.html", {"form": form})

