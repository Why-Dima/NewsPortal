from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


red = redis.Redis(
    host='redis-16719.c93.us-east-1-3.ec2.cloud.redislabs.com',
    port=16719,
    password='19P5iAltZP0iIUwAYjjmnXraMQxuTX4E'
)
