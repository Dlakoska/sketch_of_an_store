from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE,
                             verbose_name="Наименование продукта",
                             help_text="Введите название продукта")
    description = models.TextField(
        verbose_name="Описание продукта", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото товара",
    )
    category = models.CharField(
        max_length=100, verbose_name="Категория", help_text="Введите категорию продукта"
    )
    price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата создания(записи в БД)")
    updated_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата последнего изменения(записи в БД)")
    manufactured_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата производства продукта")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "-created_at"]

    def __str__(self):
        return self.name

