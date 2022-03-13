import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime
from news.models import Category, Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def news_sender():

    print('===================================ПРОВЕРКА СЕНДЕРА===================================')

    for category in Category.objects.all():

        news_from_each_category = []

        # определение номера прошлой недели
        week_number_last = datetime.now().isocalendar()[1] - 1

        for news in Post.objects.filter(category_id=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'header',
                                                                                    'dateCreation',
                                                                                    'category_id__name'):

            # преобразуем дату в человеческий вид - убираем секунды и прочую хрень
            date_format = news.get("dateCreation").strftime("%m/%d/%Y")

            # из данных запроса выдираем нужные нам поля (dateCreation - для проверки выводится), и из значений данных
            # полей формируем заголовок и реальную ссылку на переход на статью на наш сайт
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("header")}, '
                   f'Категория: {news.get("category_id__name")}, Дата создания: {date_format}')

            # каждую строчку помещаем в список новостей
            news_from_each_category.append(new)

        # для удобства в консоль добавляем разграничители и пометки
        print()
        print('+++++++++++++++++++++++++++++', category.name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("Письма будут отправлены подписчикам категории:", category.name, '( id:', category.id, ')')

        # переменная subscribers содержит информацию по подписчиках, в дальшейшем понадобится их мыло
        subscribers = category.subscribers.all()

        # этот цикл лишь для вывода инфы в консоль об адресах подписчиков, ни на что не влияет, для удобства и тестов
        print('по следующим адресам email: ')
        for qaz in subscribers:
            print(qaz.email)

        for subscriber in subscribers:
            print('____________________________', subscriber.email, '___________________________________')
            print('Письмо, отправленное по адресу: ', subscriber.email)
            html_content = render_to_string(
                'mail_sender.html', {'user': subscriber,
                                     'text': news_from_each_category,
                                     'category_name': category.name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='newspost1@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()

            # для удобства в консоль выводим содержимое нашего письма, в тестовом режиме проверим, что и
            # кому отправляем
            print(html_content)

            # Чтобы запустить реальную рассылку нужно раскоментить нижнюю строчку
            # msg.send()


# наша задача по выводу текста на экран
# def my_job():
#     #  Your job processing logic here...
#     print('hello from job')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")