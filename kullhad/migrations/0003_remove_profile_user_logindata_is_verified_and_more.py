# Generated by Django 4.0.5 on 2022-09-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullhad', '0002_profile_prof2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='logindata',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Prof2',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
