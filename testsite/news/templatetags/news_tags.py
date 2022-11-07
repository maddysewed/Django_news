from django import template

from django.db.models import *
from news.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag(filename='news/cat_list.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {"categories": categories}
