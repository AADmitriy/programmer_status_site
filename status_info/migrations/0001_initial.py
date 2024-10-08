# Generated by Django 5.0.6 on 2024-06-11 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=520, unique=True)),
                ('description', models.CharField(max_length=5110)),
                ('current', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('comprehension', models.IntegerField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=520, unique=True)),
                ('description', models.CharField(max_length=5110)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=520, unique=True)),
                ('description', models.CharField(max_length=5110)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=520, unique=True)),
                ('backend_stat', models.IntegerField()),
                ('frontend_stat', models.IntegerField()),
                ('data_science_stat', models.IntegerField()),
                ('data_base_stat', models.IntegerField()),
            ],
        ),
    ]
