# Generated by Django 5.1.1 on 2024-09-08 05:27

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='liquor',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('favorites', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileReviews',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('calification', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('cocktail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.cocktail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.profile')),
            ],
        ),
    ]
