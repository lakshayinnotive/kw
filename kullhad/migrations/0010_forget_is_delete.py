# Generated by Django 3.2.7 on 2022-09-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullhad', '0009_forget'),
    ]

    operations = [
        migrations.AddField(
            model_name='forget',
            name='is_delete',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
