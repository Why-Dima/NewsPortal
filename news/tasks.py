from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from celery.schedules import crontab


@shared_task
def send_mail_every_week(sub_username, sub_useremail, html_content):

    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}, новые статьи за прошлую неделю в вашем разделе!',
        from_email='newspost1@yandex.ru',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')

    msg.send()

