# Generated by Django 3.1 on 2020-08-12 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agreement',
            field=models.CharField(choices=[('AL', 'Allowed'), ('DIS', 'Disallowed')], default='DIS', max_length=3),
        ),
    ]
