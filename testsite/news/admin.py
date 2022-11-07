from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin, NewsAdminForm):
    form = NewsAdminForm
    list_display = ["id", "title", "date", "is_published", "category", "get_photo"]
    list_display_links = ["title"]
    search_fields = ["title", "content"]
    list_editable = ("is_published", "category")
    list_filter = ("title", "date", "category")
    fields = ["title", "content", "category", "photo", "date", "is_published", "get_photo"]
    readonly_fields = ["date", "is_published", "get_photo"]

    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return "-"

    get_photo.short_description = "Фото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]
    search_fields = ["name"]


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = "Управление новостями"
admin.site.site_header = "Управление новостями"
