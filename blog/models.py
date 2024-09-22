from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок",
                             help_text="Введите название продукта")

    slug = models.CharField(max_length=100, verbose_name="slug", null=True, blank=True)

    description = models.TextField(
        verbose_name="Содержимое", help_text="Введите содержимое блога"
    )

    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )

    created_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата создания(записи в БД)")
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="количество просмотров")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title", "-created_at"]

    def __str__(self):
        return self.title
