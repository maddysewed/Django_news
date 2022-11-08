from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    #path('', index, name="home"),
    path('', HomeNews.as_view(), name="home"),
    #path('categories/<int:category_id>/', get_category, name="categories"),
    # path('categories/<int:category_id>/', cache_page(60 * 5)(NewsOfCategory.as_view()), name="categories"),
    path('categories/<int:category_id>/', NewsOfCategory.as_view(), name="categories"),
    # path('news/<int:news_id>/', get_news, name="news_item"),
    path('news/<int:pk>/', ViewNews.as_view(), name="news_item"),
    # path('news/add-news/', add_news, name="add_news"),
    path('news/add-news/', CreateNews.as_view(), name="add_news"),
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('mail-to-user/', send_mails_to_user, name="send_mails_to_user"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]