# Generated by Django 3.1.7 on 2021-03-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=50, unique=True, verbose_name='uid')),
                ('subject', models.CharField(max_length=50, verbose_name='科目名')),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('description', models.TextField(blank=True, null=True, verbose_name='説明')),
                ('begin_at', models.DateTimeField(blank=True, null=True, verbose_name='開始日時')),
                ('end_at', models.DateTimeField(blank=True, null=True, verbose_name='終了日時')),
                ('last_modified_at', models.DateTimeField(blank=True, null=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name_plural': 'Event',
            },
        ),
    ]
