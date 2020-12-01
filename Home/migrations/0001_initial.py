# Generated by Django 3.0.5 on 2020-11-10 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Big5result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openness', models.FloatField(blank=True, null=True)),
                ('conscientiousness', models.FloatField(blank=True, null=True)),
                ('extraversion', models.FloatField(blank=True, null=True)),
                ('agreeableness', models.FloatField(blank=True, null=True)),
                ('neuroticism', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
