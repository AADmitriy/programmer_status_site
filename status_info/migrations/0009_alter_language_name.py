# Generated by Django 5.0.6 on 2024-07-03 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status_info', '0008_alter_job_description_alter_job_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
