# Generated by Django 5.0.6 on 2024-06-15 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status_info', '0004_quest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('description', models.CharField(max_length=5110)),
                ('gains', models.CharField(max_length=5110)),
            ],
        ),
    ]
