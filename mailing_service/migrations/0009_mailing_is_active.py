# Generated by Django 4.2.5 on 2023-10-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_service', '0008_alter_client_options_alter_mailing_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активность рассылки'),
        ),
    ]