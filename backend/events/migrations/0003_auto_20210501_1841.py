# Generated by Django 3.2 on 2021-05-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20210310_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.AddField(
            model_name='event',
            name='notified_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='通知日時'),
        ),
    ]
