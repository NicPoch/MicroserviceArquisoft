# Generated by Django 3.1.3 on 2020-12-06 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Security', '0002_auto_20201202_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='username',
            field=models.TextField(default=None, unique=True),
        ),
    ]