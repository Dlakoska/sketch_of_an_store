from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(models.Model):
    username = models.CharField(
        max_length=50,
        verbose_name="Имя пользователя",
        help_text="Введите имя пользователя",
    )
    avatar = models.ImageField(
        upload_to="blog/avatar", verbose_name="Аватар пользователя", **NULLABLE
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите электронную почту",
    )
    country = models.CharField(max_length=15, verbose_name="Страна", **NULLABLE)

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок",
                             help_text="Введите название продукта")

    slug = models.CharField(max_length=100, verbose_name="slug", **NULLABLE)

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
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        **NULLABLE,
        related_name="articles",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title", "-created_at"]

    def __str__(self):
        return self.title
