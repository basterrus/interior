from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.DOMAIN_NAME}{verify_link}'
    print(settings.DOMAIN_NAME)
    message = f'Ссылка для активации вашей учетной записи:  {full_link}'

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
