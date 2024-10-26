from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied

from catalog.services import get_category_from_cache


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        products_with_versions = []
        # Пройдитесь по каждому продукту и извлеките его активную версию
        for product in self.object_list:
            active_version = product.version.filter(
                is_current=True).first()  # Используйте "version" вместо "version_set"
            products_with_versions.append({
                'product': product,
                'active_version': active_version
            })
        context_data['products_with_versions'] = products_with_versions
        return context_data

    def get_queryset(self):
        key = "product_list"
        return get_category_from_cache(Product, key)


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)  # пока не сохраняем данные в базе
            self.object.owner = self.request.user  # привязываем текущего пользователя к продукту
            self.object.save()  # сохраняем данные в базе

            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data
    
    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ProductForm
        if (user.has_perm('catalog.can_edit_is_active') and user.has_perm('catalog.can_edit_description')
                and user.has_perm('catalog.can_edit_category')):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    model = Product
    success_url = reverse_lazy('catalog:product_list')


class HomePageView(TemplateView):
    template_name = 'catalog/home.html'


class ContactPageView(TemplateView):
    template_name = 'catalog/contacts.html'


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        key = "category_list"
        return get_category_from_cache(Category, key)
