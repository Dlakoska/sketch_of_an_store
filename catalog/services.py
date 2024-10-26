from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_category_from_cache(model, key):
    if not CACHE_ENABLED:
        return model.objects.all()

    model_list = cache.get(key)
    if model_list is not None:
        return model_list
    model_list = model.objects.all()
    cache.set(key, model_list)
    return model_list
