from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Контент")  # blank=True  поле не обязательно к заполнению
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")  # year, month, day
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категория")
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("news_item", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ("-date", "title")


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")

    def get_absolute_url(self):
        return reverse("categories", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name", )
