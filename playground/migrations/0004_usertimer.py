# Generated by Django 4.2.15 on 2024-08-23 05:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0003_remove_user_score_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimer',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('remaining_time', models.IntegerField(default=300)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
