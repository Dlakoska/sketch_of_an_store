import random
import string
import secrets
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/email_confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)  # Hash the new password
            user.save()

            # Send email with the new password
            send_mail(
                subject='Ваш новый пароль',
                message=f'Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )

            messages.success(request, 'Новый пароль отправлен на ваш адрес электронной почты.')
            return redirect('users:login')  # Redirect to login page after successful reset

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким адресом электронной почты не найден.')

    return render(request, 'users/reset_password.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
