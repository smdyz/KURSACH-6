import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DetailView

from users.forms import UserProfileForm, UserRegisterForm
from users.models import User

# Create your views here.
CHARS = '+-*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = ''
        for i in range(10):
            token += random.choice(CHARS)
        form.verified_pass = token
        user = form.save()
        user.token = token
        send_mail(
            subject='Верификация почты',
            message=f'Поздравляем с регистрацией в сервисе ЯРассылки \n'
                    f'Для завершения регистрации перейдите по ссылке: \n'
                    f'http://127.0.0.1:8000/users/confirm/{user.token} \n'
                    f'Если вы не причастны к регистации - игнорируйте это письмо.\n'
                    f'С Уважением, команда ЯРассылки',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def verify_view(request, token):
    user = User.objects.get(token=token)
    user.is_verified = True
    user.save()
    return render(request, 'users/user_verify.html')


def res_password(request):
    new_password = ''
    if request.method == 'POST':
        email = request.POST['email']
        user = get_object_or_404(User, email=email)
        for i in range(10):
            new_password += random.choice(CHARS)
        send_mail(
            subject='Смена пароля',
            message=f'Ваш новый пароль {new_password}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')


class UsersView(ListView):
    model = User
    template_name = 'manager/users_list.html'
    context_object_name = 'objects_list'


class UsersDetail(DetailView):
    model = User
    template_name = 'manager/users_detail.html'
    context_object_name = 'objects_list'


def block_user(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if request.user.is_staff and user_item.is_superuser:
        rendered = render_to_string('manager/403_forbidden.html')
        return HttpResponse(rendered, status=403)
    if user_item.is_blocked:
        user_item.is_blocked = False
    else:
        user_item.is_blocked = True
    user_item.save()
    return redirect(reverse('users:manager_users'))