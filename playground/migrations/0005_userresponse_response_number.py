# Generated by Django 4.2.15 on 2024-08-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0004_usertimer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='response_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
