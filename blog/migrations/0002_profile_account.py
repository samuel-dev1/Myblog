# Generated by Django 3.2.23 on 2024-01-05 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account',
            field=models.IntegerField(blank=True, default=810423221, unique=True),
        ),
    ]
