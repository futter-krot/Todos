# Generated by Django 2.2.10 on 2021-06-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20210612_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='category',
            field=models.ManyToManyField(blank=True, default=1, to='tasks.Category'),
        ),
    ]