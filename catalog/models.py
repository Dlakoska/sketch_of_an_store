from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование категории"
    )
    description = models.TextField(
        verbose_name="Описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование продукта"
    )
    description = models.TextField(
        verbose_name="Описание продукта"
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Фото"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="products",
        blank=True,
        null=True,
    )
    price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата создания(записи в БД)"
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата последнего изменения(записи в БД)"
    )
    owner = models.ForeignKey(User, verbose_name="Владелец",
                              on_delete=models.SET_NULL, **NULLABLE)

    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "-created_at"]
        permissions = [
            ("can_edit_is_active", "Can edit is_active"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_category", "Can edit category")
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название версии"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        related_name="version"
    )
    version_number = models.PositiveIntegerField(verbose_name="Версия")
    is_current = models.BooleanField(blank=True, null=True, verbose_name='текущая версия')

    def __str__(self):
        return f'Продукт - {self.product}, версия - {self.name}'

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
