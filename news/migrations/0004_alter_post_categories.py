# Generated by Django 4.0.1 on 2022-03-08 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ForeignKey(default='кино', null=True, on_delete=django.db.models.deletion.CASCADE, to='news.category'),
        ),
    ]