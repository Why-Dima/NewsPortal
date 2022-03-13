from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.shortcuts import redirect
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).categories.pk)
    text = instance.text
    post = instance
    subscribers = category.subscribers.all()
    for subscriber in subscribers:
        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': text[:50], 'post': post})
        msg = EmailMultiAlternatives(subject=f'{subscriber.username}', from_email='newspost1@yandex.ru',
                                     to=[subscriber.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

