# Generated by Django 3.2.23 on 2023-12-19 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('ranting', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('CommentPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='blog.updatepost')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]
