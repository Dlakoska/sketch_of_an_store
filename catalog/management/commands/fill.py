import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        # Здесь мы получаем данные из фикстуры с категориями
        with open('catalog.json', 'r', encoding='utf-8') as file:
            file = json.load(file)
            categories = []
            for category in file:
                if category['model'] == 'catalog.category':
                    category['fields']['pk'] = category['pk']
                    categories.append(category['fields'])
            return categories

    @staticmethod
    def json_read_products():
        # Здесь мы получаем данные из фикстурв с продуктами
        with open('catalog.json', 'r', encoding='utf-8') as file:
            file = json.load(file)
            products = []
            for product in file:
                if product['model'] == 'catalog.product':
                    product['fields']['category'] = product['pk']
                    products.append(product['fields'])
            return products

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()

        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(**category)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(name=product['name'],
                        description=product['description'],
                        image=product['image'],
                        category=Category.objects.get(pk=product['category']),
                        price=product['price'],
                        created_at=product['created_at'],
                        updated_at=product['updated_at'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)