# Generated by Django 3.0.3 on 2020-02-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200211_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='surname',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default=' ', max_length=15),
        ),
    ]
